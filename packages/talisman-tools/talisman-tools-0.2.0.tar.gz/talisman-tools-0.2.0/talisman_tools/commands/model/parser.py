from argparse import ArgumentParser, Namespace
from typing import Callable

from talisman_tools.arguments.proceessor import get_processor_factory
from talisman_tools.parser_helper import configure_subparsers
from .commands import SUBPARSERS


def configure_model_parser(parser: ArgumentParser, extra_actions: Callable[[Namespace], None]) -> None:
    processor_factory = get_processor_factory(parser)

    def get_action() -> Callable[[Namespace], None]:
        def action(args: Namespace):
            extra_actions(args)
            args.processor_action()(processor_factory(args), args)

        return action

    parser.set_defaults(action=get_action)

    configure_subparsers(parser, SUBPARSERS)
