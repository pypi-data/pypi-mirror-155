from argparse import ArgumentParser, Namespace
from typing import Callable, Dict, Set, Tuple

from talisman_tools.plugin.cli import add_extra_cli_arguments


def configure_subparsers(
        parser: ArgumentParser,
        subparsers: Dict[str, Tuple[str, Callable[[ArgumentParser, Callable[[Namespace], None]], None]]]
) -> None:
    subparsers_handler = parser.add_subparsers(help='Available sub-commands')
    for subparser_name, (description, configure) in subparsers.items():
        subparser = subparsers_handler.add_parser(subparser_name, help=description)
        extra_actions = add_extra_cli_arguments(subparser, subparser_name)
        configure(subparser, _group_actions(extra_actions))


def _group_actions(actions: Set[Callable[[Namespace], None]]) -> Callable[[Namespace], None]:
    def grouped_action(args: Namespace) -> None:
        for action in actions:
            action(args)
    return grouped_action
