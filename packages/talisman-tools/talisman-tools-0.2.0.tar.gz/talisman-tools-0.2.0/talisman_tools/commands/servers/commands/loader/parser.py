from argparse import ArgumentParser, Namespace
from typing import Callable

from fastapi import FastAPI


def configure_loader_parser(parser: ArgumentParser, extra_actions: Callable[[Namespace], None]) -> None:
    def get_action() -> Callable[[Namespace], FastAPI]:
        def action_with_extra(args: Namespace) -> FastAPI:
            from .action import action
            extra_actions(args)
            return action(args)
        return action_with_extra

    parser.set_defaults(server_action=get_action)
