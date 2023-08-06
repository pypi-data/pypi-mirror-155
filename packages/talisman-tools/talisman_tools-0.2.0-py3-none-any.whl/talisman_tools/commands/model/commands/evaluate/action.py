import json
from functools import partial
from itertools import chain
from typing import Dict

from tdm.datamodel import ConceptFact, TalismanDocument, ValueFact

from talisman_tools.commands.model.commands.evaluate.disambiguation_quality import evaluate_dmb
from talisman_tools.commands.model.commands.evaluate.evaluation import evaluate_nerc, evaluate_relext, evaluate_relext_upper_bound
from tp_interfaces.abstract import AbstractDocumentProcessor
from tp_interfaces.helpers.io import read_json
from tp_interfaces.readers.abstract import AbstractReader


def print_scores(scores: Dict[str, dict]):
    def round_floats(val, precision=4):
        if isinstance(val, float):
            return round(val, precision)
        if isinstance(val, dict):
            return {k: round_floats(v) for k, v in val.items()}
        raise ValueError

    def stringify_keys(d: dict):
        ret = {}
        for key, val in d.items():
            if isinstance(key, (tuple, frozenset)):
                key = str(key)
            if isinstance(val, dict):
                val = stringify_keys(val)

            ret[key] = val

        return ret

    json_repr = json.dumps(stringify_keys(round_floats(scores)), sort_keys=True, indent=2)
    print(json_repr)


def keep_nerc(doc: TalismanDocument) -> TalismanDocument:
    facts = chain(
        map(lambda f: f.with_changes(value=tuple()), doc.filter_facts(ConceptFact)),  # TODO: replace value with None instead of empty tuple
        doc.filter_facts(ValueFact)
    )
    return doc.without_facts().with_facts(facts)


def clear_values(doc: TalismanDocument) -> TalismanDocument:
    return doc.with_facts(
        map(lambda f: f.with_changes(value=tuple()), doc.filter_facts(ConceptFact)),  # TODO: replace value with None instead of empty tuple
    )


mode = {
    "all": lambda doc: doc.without_facts(),  # start from clear document (no facts provided)
    "nerc": lambda doc: doc.without_facts(),  # start from clear document (no facts provided)
    "relext": keep_nerc,  # start from document with concept and value facts (no link facts, no fact values)
    "dmb": clear_values,  # start from document with facts without values
}

evaluators = {
    'all': {
        'nerc': evaluate_nerc,
        'relext': evaluate_relext,
        'relext-upper-bound': evaluate_relext_upper_bound,
        'dmb': partial(evaluate_dmb, at_ks=[1, 2, 3])  # TODO: make configurable from cli
    },
    'relext': {
        'relext': evaluate_relext,
        'relext-upper-bound': evaluate_relext_upper_bound,
        'dmb': partial(evaluate_dmb, at_ks=[1, 2, 3])  # TODO: make configurable from cli
    },
    'nerc': {
        'nerc': evaluate_nerc
    },
    'dmb': {
        'dmb': partial(evaluate_dmb, at_ks=[1, 2, 3])  # TODO: make configurable from cli
    }
}


def evaluate(processor: AbstractDocumentProcessor, eval_mode: str, reader: AbstractReader, config_path):
    gold_docs = tuple(reader.read())
    actual_docs = tuple(map(mode[eval_mode], gold_docs))

    with processor:
        processor_config_type = processor.config_type
        config = processor_config_type.parse_obj(read_json(config_path)) if config_path else processor_config_type()
        actual_docs = processor.process_docs(actual_docs, config)

    scores = {name: evaluate(actual_docs, gold_docs) for name, evaluate in evaluators[eval_mode].items()}

    print_scores(scores)
