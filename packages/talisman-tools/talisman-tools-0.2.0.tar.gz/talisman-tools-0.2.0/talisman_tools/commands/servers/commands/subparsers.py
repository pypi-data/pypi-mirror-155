from argparse import ArgumentParser, Namespace
from typing import Callable, Dict, Tuple

from talisman_tools.commands.servers.commands.loader import configure_loader_parser
from talisman_tools.commands.servers.commands.processor import configure_processor_parser

# Every subcommand should have its own parser with description
# Note that subparsers should change the default `server_action` argument
SUBPARSERS: Dict[str, Tuple[str, Callable[[ArgumentParser, Callable[[Namespace], None]], None]]] = {
    'loader': ('Configure loader server', configure_loader_parser),
    'processor': ('Configure processor server', configure_processor_parser)
}
