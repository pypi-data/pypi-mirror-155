from argparse import ArgumentParser, Namespace
from typing import Callable

from tp_interfaces.readers.abstract import AbstractReader


def configure_analyse_ambiguity_parser(parser: ArgumentParser, extra_actions: Callable[[Namespace], None]) -> None:

    def get_action() -> Callable[[AbstractReader, Namespace], None]:
        def action(reader: AbstractReader, args: Namespace) -> None:
            from tp_interfaces.knowledge_base.manager import KBManager
            from .action import analyse_ambiguity

            extra_actions(args)
            analyse_ambiguity(KBManager().knowledge_base, reader.read())

        return action

    parser.set_defaults(dataset_action=get_action)
