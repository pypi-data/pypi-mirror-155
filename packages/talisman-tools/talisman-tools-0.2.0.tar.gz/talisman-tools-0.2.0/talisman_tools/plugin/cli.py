from argparse import ArgumentParser, Namespace
from itertools import chain
from typing import Callable, Set

from .abstract import AbstractPluginManager


class CLIPluginManager(AbstractPluginManager):
    def __init__(self):
        AbstractPluginManager.__init__(self, 'CLI_OPTIONS')

    @staticmethod
    def _check_value(value) -> bool:
        return isinstance(value, set)  # TODO: improve validation


def add_extra_cli_arguments(parser: ArgumentParser, parser_name: str) -> Set[Callable[[Namespace], None]]:
    from talisman_tools.plugin import CLIPlugins
    actions = set()
    for cli_factory in chain.from_iterable(CLIPlugins.plugins.values()):
        action = cli_factory(parser, parser_name)
        if action:
            actions.add(action)
    return actions
