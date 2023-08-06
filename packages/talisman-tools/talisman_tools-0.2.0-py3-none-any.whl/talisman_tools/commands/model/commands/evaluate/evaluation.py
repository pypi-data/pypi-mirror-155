from collections import defaultdict
from functools import partial
from itertools import chain, zip_longest
from typing import Any, Callable, Dict, Iterable, Iterator, NamedTuple, Set, Tuple, Type

from tdm.abstract.datamodel import AbstractFact
from tdm.abstract.datamodel.fact import AbstractLinkValue
from tdm.datamodel import TalismanDocument, TalismanSpan
from tdm.datamodel.fact import ConceptFact, PropertyFact, RelationFact, ValueFact

from .metrics import ir_categorized_queries_score, ir_macro_scores, ir_micro_scores


def _scores2dict(precision: float, recall: float, f1: float):
    return {"precision": float(precision), "recall": float(recall), "f1": float(f1)}


def _with_prefix(d: Dict[str, Any], prefix: str) -> dict:
    return {f"{prefix}_{k}": v for k, v in d.items()}


def _evaluate(
        predicted: Iterable[TalismanDocument],
        gold: Iterable[TalismanDocument],
        objects_getter: Callable[[TalismanDocument], Iterable[Any]],
        categorizers: Dict[str, Callable]
) -> Dict[str, dict]:

    queries = []
    predicted_objects, gold_objects = [], []

    for pred_doc, gold_doc in zip_longest(predicted, gold):
        if pred_doc is None or gold_doc is None:
            raise ValueError("Predicted and gold doocuments iterables length mismatch")

        if pred_doc.content.text != gold_doc.content.text:
            raise ValueError("Predicted and gold documents have different texts")

        predicted_objects.append(set(objects_getter(pred_doc)))
        gold_objects.append(set(objects_getter(gold_doc)))
        queries.append(gold_doc.content.text)

    macro_scores = _scores2dict(*ir_macro_scores(predicted_objects, gold_objects))
    micro_scores = _scores2dict(*ir_micro_scores(predicted_objects, gold_objects))
    final_scores = {**_with_prefix(macro_scores, "macro"), **_with_prefix(micro_scores, "micro"), "categories": {}}

    for categorizer_name, categorizer in categorizers.items():
        category_scores = defaultdict(dict)

        for strategy_name, strategy in [("micro", ir_micro_scores), ("macro", ir_macro_scores)]:
            scores: Dict[str, Tuple[float, float, float]] = ir_categorized_queries_score(
                queries, predicted_objects, gold_objects, categorizer, strategy)
            scores: Dict[str, Dict[str, float]] = {k: _with_prefix(_scores2dict(*vals), strategy_name) for k, vals in scores.items()}
            for key, val in scores.items():
                category_scores[key].update(val)

        final_scores["categories"][categorizer_name] = dict(category_scores)

    return final_scores


class FactTupleView(NamedTuple):
    fact_type: str
    type_id: str
    mention: Tuple[TalismanSpan]


class LinkTupleView(NamedTuple):
    fact_type: str
    type_id: str
    from_fact: FactTupleView
    to_fact: FactTupleView


def _fact_type(query, fact: NamedTuple) -> str:
    return fact.type_id


def _source_target_types(query, link_fact: LinkTupleView) -> Tuple[str, str]:
    return link_fact.from_fact.type_id, link_fact.to_fact.type_id


def _link_signature(query, link_fact: LinkTupleView) -> Tuple[str, str, str]:
    return link_fact.from_fact.type_id, link_fact.to_fact.type_id, link_fact.type_id


_NERC_CATEGORIZERS = {
    "fact_type": _fact_type
}

_LINK_CATEGORIZERS = {
    "fact_type": _fact_type,
    "source_target_types": _source_target_types,
    "signature": _link_signature
}


def _extract_facts(doc: TalismanDocument, types: Set[Type[AbstractFact]], filter_=lambda _: True) -> Iterator[AbstractFact]:
    return chain.from_iterable(map(partial(doc.filter_facts, filter_=filter_), types))


def _fact_tuple_view(fact: AbstractFact) -> FactTupleView:
    return FactTupleView(fact.fact_type, fact.type_id, fact.mention if fact.mention is not None else tuple())


def _extract_entity_objects(doc: TalismanDocument) -> Iterable[tuple]:
    return map(_fact_tuple_view, _extract_facts(doc, {ConceptFact, ValueFact}))


def evaluate_nerc(predicted: Iterable[TalismanDocument], gold: Iterable[TalismanDocument]) -> Dict[str, dict]:
    return _evaluate(predicted, gold, _extract_entity_objects, _NERC_CATEGORIZERS)


def _link_fact_tuple_view(fact: AbstractFact[AbstractLinkValue]) -> LinkTupleView:
    return LinkTupleView(fact.fact_type, fact.type_id, _fact_tuple_view(fact.value.from_fact), _fact_tuple_view(fact.value.to_fact))


def _extract_relation_objects(doc: TalismanDocument) -> Iterable[tuple]:
    return map(_link_fact_tuple_view, _extract_facts(doc, {RelationFact, PropertyFact}))


def evaluate_relext(predicted: Iterable[TalismanDocument], gold: Iterable[TalismanDocument]) -> Dict[str, dict]:
    return _evaluate(predicted, gold, _extract_relation_objects, _LINK_CATEGORIZERS)


def evaluate_relext_upper_bound(predicted: Iterable[TalismanDocument], gold: Iterable[TalismanDocument]) -> Dict[str, dict]:
    predicted, gold = tuple(predicted), tuple(gold)
    predicted_w_gold_rels = []

    for pred_doc, gold_doc in zip_longest(predicted, gold):
        gold_doc: TalismanDocument
        if pred_doc is None or gold_doc is None:
            raise ValueError("Predicted and gold doocuments iterables length mismatch")

        pred_entity_facts = set(map(_fact_tuple_view, _extract_facts(pred_doc, {ConceptFact, ValueFact})))
        gold_entity_facts = set(_extract_facts(gold_doc, {ConceptFact, ValueFact}, lambda f: _fact_tuple_view(f) in pred_entity_facts))

        def filter_(fact: AbstractFact[AbstractLinkValue]) -> bool:
            return fact.value.from_fact in gold_entity_facts and fact.value.to_fact in gold_entity_facts

        possible_to_find_gold_rels = _extract_facts(gold_doc, {RelationFact, PropertyFact}, filter_)

        predicted_w_gold_rels.append(
            gold_doc.without_facts().with_facts(chain(gold_entity_facts, possible_to_find_gold_rels))
        )

    return evaluate_relext(predicted_w_gold_rels, gold)


def evaluate_ie(predicted: Iterable[TalismanDocument], gold: Iterable[TalismanDocument]) -> Dict[str, dict]:
    """
    Currently evaluates only nerc, relext and relext upper bound with provided facts
    """
    predicted, gold = tuple(predicted), tuple(gold)
    return {
        "nerc": evaluate_nerc(predicted, gold),
        "relext": evaluate_relext(predicted, gold),
        "relext_upper_bound": evaluate_relext_upper_bound(predicted, gold)
    }
