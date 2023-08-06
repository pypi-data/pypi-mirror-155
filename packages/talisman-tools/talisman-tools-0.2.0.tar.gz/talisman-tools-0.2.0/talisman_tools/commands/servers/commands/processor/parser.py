from argparse import ArgumentParser, Namespace
from typing import Callable

from fastapi import FastAPI

from talisman_tools.arguments.proceessor import get_processor_factory
from talisman_tools.plugin import TDMPlugins


def configure_processor_parser(parser: ArgumentParser, extra_actions: Callable[[Namespace], None]) -> None:
    parser.add_argument('-dm', type=str, choices=set(TDMPlugins.plugins), metavar='<document model>')
    processor_factory = get_processor_factory(parser)

    def get_action() -> Callable[[Namespace], FastAPI]:
        def action_with_extra(args: Namespace) -> FastAPI:
            from .action import action
            extra_actions(args)
            return action(args, processor_factory)
        return action_with_extra

    parser.set_defaults(server_action=get_action)
