import json
import logging
from argparse import Namespace
from collections import defaultdict
from itertools import chain
from pathlib import Path
from typing import Dict, Iterable, Iterator, Optional, Tuple

from more_itertools import ichunked
from tdm.datamodel import TalismanDocument

from talisman_tools.plugin import ReaderPlugins
from talisman_tools.talisman_logging import configure_json_logging
from tp_interfaces.helpers.io import read_json
from tp_interfaces.knowledge_base.interfaces import DBConcept
from tp_interfaces.knowledge_base.manager import KBManager
from tp_interfaces.knowledge_base.readers import JSONConceptReader, TypesMappingFilteringReader


logger = logging.getLogger(__name__)


def merge_concepts(concepts: Iterable[DBConcept], cro: Dict[str, int], name_wo_id: bool) -> Tuple[DBConcept, ...]:

    id2name_type = {}
    id2aliases = defaultdict(list)
    id2out_relations = defaultdict(list)
    id2properties = defaultdict(list)
    id2type = defaultdict(type)
    errors = []
    for concept in concepts:
        if concept.id_ in id2name_type:
            name, type_ = id2name_type[concept.id_]
            concept_name = concept.name if name_wo_id else f"{concept.name} ({concept.id_})"
            if concept_name != name or concept.type != type_:
                old_priority = cro.get(type_, float('inf'))
                new_priority = cro.get(concept.type, float('inf'))
                if new_priority > old_priority:
                    continue  # ignore concept with low priority
                elif new_priority < old_priority:
                    id2name_type[concept.id_] = (concept_name, concept.type)
                    del id2aliases[concept.id_]
                    del id2out_relations[concept.id_]
                    del id2properties[concept.id_]
                else:
                    errors.append(f"{concept.id_}: ({name}, {type_}) != ({concept_name}, {concept.type})")
        else:
            id2name_type[concept.id_] = (concept.name if name_wo_id else f"{concept.name} ({concept.id_})", concept.type)
        id2type[concept.id_] = type(concept)
        id2aliases[concept.id_].extend(concept.aliases)
        id2out_relations[concept.id_].extend(concept.out_relations)
        id2properties[concept.id_].extend(concept.properties)

    if errors:
        raise ValueError("Different objects with same id: " + '\n'.join(errors))

    id2in_relations = defaultdict(list)
    for out_relations in id2out_relations.values():
        for relation in out_relations:
            id2in_relations[relation.target_id].append(relation)

    return tuple(id2type[id_](id_, name, type_, id2aliases[id_], id2in_relations[id_], id2out_relations[id_], id2properties[id_])
                 for id_, (name, type_) in id2name_type.items())


def unique_documents(documents: Iterable[TalismanDocument]) -> Iterator[TalismanDocument]:
    names = set()
    for document in documents:
        if document.doc_id not in names:
            names.add(document.doc_id)
            yield document
        else:
            logger.warning(f"Duplicate document with name: {document.doc_id}")


def read_cro(path: Optional[Path]) -> Dict[str, int]:
    if path is None:
        return {}
    with path.open('r', encoding='utf-8') as f:
        return {t: i for i, t in enumerate(json.load(f))}


def action(args: Namespace):
    readers = ReaderPlugins.flattened

    if len(args.concepts_mapping_docs) % 3 != 0:
        raise Exception('Expected <path to jsonl serialized concepts> <path to types mapping config> <path to gold docs with concepts>')

    configure_json_logging()

    concepts = []
    docs = []

    for concepts_path, types_mapping_path, docs_path, in ichunked(args.concepts_mapping_docs, 3):
        reader = JSONConceptReader(Path(concepts_path))
        if types_mapping_path != '_':
            reader = TypesMappingFilteringReader.from_config(reader, read_json(types_mapping_path))
        concepts.append(reader.read())
        docs.append(readers["default"](Path(docs_path)).read())

    cro = read_cro(args.conflict_resolution_order)

    concepts = merge_concepts(chain.from_iterable(concepts), cro, args.concept_name_wo_id)
    docs = unique_documents(chain.from_iterable(docs))

    kb = KBManager().knowledge_base
    with kb:
        kb.load_new_concepts_and_mentions(concepts, map(lambda doc: doc.content, docs))
