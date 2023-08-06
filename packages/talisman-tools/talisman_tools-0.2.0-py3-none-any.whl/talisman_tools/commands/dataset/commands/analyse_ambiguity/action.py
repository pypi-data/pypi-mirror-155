from collections import Counter
from operator import itemgetter
from typing import Iterator, Tuple

from tdm.abstract.datamodel import AbstractTalismanDocument
from tdm.datamodel import ConceptFact

from tp_interfaces.knowledge_base.interfaces import DisambiguationKB


def _count_freqs(kb: DisambiguationKB, docs: Iterator[AbstractTalismanDocument]) -> Tuple[Counter, Counter, int]:
    not_in_kb_cands_freqs, in_kb_cands_freqs, in_kb_in_candidates = Counter(), Counter(), 0

    for doc in docs:
        candidates = kb.get_candidates(doc)
        for fact in doc.filter_facts(ConceptFact):
            gold_concept = fact.value
            concept_cands_len = len(candidates[fact].candidates) if fact in candidates else 0

            if gold_concept is None:
                counter_to_adjust = not_in_kb_cands_freqs
            else:
                counter_to_adjust = in_kb_cands_freqs
                if fact in candidates and gold_concept in map(lambda dbc: dbc.id_, candidates[fact].candidates):
                    in_kb_in_candidates += 1

            counter_to_adjust[concept_cands_len] += 1

    return not_in_kb_cands_freqs, in_kb_cands_freqs, in_kb_in_candidates


def _percent_str(val: int, ovrl: int) -> str:
    return f"{100 * val / ovrl:5.2f}%"


def _print_freqs(freqs: Counter) -> None:
    ovrl_sum = sum(freqs.values())
    running_sum = 0

    print("Candidates number\tMentions with this candidates number\tPercent of overall\tRunning percent")
    for cand_len, value in sorted(freqs.items(), key=itemgetter(0)):
        running_sum += value
        print(f"{cand_len}\t{value}\t{_percent_str(value, ovrl_sum)}\t{_percent_str(running_sum, ovrl_sum)}")


def analyse_ambiguity(kb: DisambiguationKB, docs: Iterator[AbstractTalismanDocument]):
    with kb:
        not_in_kb_cands_freqs, in_kb_cands_freqs, in_kb_in_candidates = _count_freqs(kb, docs)

    not_in_kb_mentions = sum(not_in_kb_cands_freqs.values())
    in_kb_mentions = sum(in_kb_cands_freqs.values())
    ovrl_mentions = not_in_kb_mentions + in_kb_mentions

    print(f"Mentions ovrl count = {ovrl_mentions}")
    print(f"InKB mentions = {in_kb_mentions} ({_percent_str(in_kb_mentions, ovrl_mentions)})")
    print(f"InKB mentions possible to disambiguate = {in_kb_in_candidates}"
          f" ({_percent_str(in_kb_in_candidates, in_kb_mentions)} out of InKB mentions)"
          f" ({_percent_str(in_kb_in_candidates, ovrl_mentions)} out of ovrl count)")
    print(f"NotInKB mentions = {not_in_kb_mentions} ({_percent_str(not_in_kb_mentions, ovrl_mentions)})")

    print("=" * 80)
    print("InKB frequencies\n")
    _print_freqs(in_kb_cands_freqs)
    print("=" * 80)
    print("NotInKb frequencies\n")
    _print_freqs(not_in_kb_cands_freqs)
