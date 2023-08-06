from argparse import ArgumentParser, Namespace
from typing import Callable, Set

from talisman_tools.arguments.reader import get_reader_factory
from talisman_tools.commands.dataset.commands import SUBPARSERS
from talisman_tools.parser_helper import configure_subparsers


def configure_dataset_parser(parser: ArgumentParser, extra_actions: Set[Callable[[Namespace], None]]) -> None:
    reader_factory = get_reader_factory(parser)

    def get_action() -> Callable[[Namespace], None]:
        def action(args: Namespace) -> None:
            for extra_action in extra_actions:
                extra_action(args)
            args.dataset_action()(reader_factory(args), args)
        return action

    parser.set_defaults(action=get_action)
    configure_subparsers(parser, SUBPARSERS)
