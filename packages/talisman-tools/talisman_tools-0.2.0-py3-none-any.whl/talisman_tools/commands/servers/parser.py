from argparse import ArgumentParser, Namespace
from typing import Callable

from talisman_tools.commands.servers.arguments.server import uvicorn_server_factory
from talisman_tools.commands.servers.commands import SUBPARSERS
from talisman_tools.parser_helper import configure_subparsers


def configure_server_parser(parser: ArgumentParser, extra_actions: Callable[[Namespace], None]) -> None:
    launcher = uvicorn_server_factory(parser)

    def get_action() -> Callable[[Namespace], None]:
        def action(args: Namespace) -> None:
            extra_actions(args)
            fast_api = args.server_action()(args)
            launcher(fast_api, args)

        return action

    parser.set_defaults(action=get_action)

    configure_subparsers(parser, SUBPARSERS)
