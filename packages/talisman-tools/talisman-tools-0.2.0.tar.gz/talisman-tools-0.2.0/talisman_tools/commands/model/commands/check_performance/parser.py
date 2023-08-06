from argparse import ArgumentParser, Namespace
from typing import Callable

from talisman_tools.arguments.reader import get_reader_factory
from tp_interfaces.abstract import AbstractDocumentProcessor


def configure_check_performance_parser(parser: ArgumentParser, extra_actions: Callable[[Namespace], None]) -> None:
    reader_factory = get_reader_factory(parser)

    parser.add_argument('count', type=int, metavar='<launch count>', default=1)

    def get_action() -> Callable[[AbstractDocumentProcessor, Namespace], None]:
        def action(processor: AbstractDocumentProcessor, args: Namespace):
            from .action import measure_time

            extra_actions(args)
            docs = tuple(reader_factory(args).read())
            with processor:
                measure_time(docs, processor, args.count)

        return action

    parser.set_defaults(processor_action=get_action)
