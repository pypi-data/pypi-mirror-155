from argparse import ArgumentParser, Namespace
from typing import Callable, Dict, Tuple

from talisman_tools.commands.dataset.commands.analyse_ambiguity import configure_analyse_ambiguity_parser
from talisman_tools.commands.dataset.commands.convert import configure_convert_parser

# Note that subparsers should change the default `dataset_action` argument
SUBPARSERS: Dict[str, Tuple[str, Callable[[ArgumentParser, Callable[[Namespace], None]], None]]] = {
    'analyse_ambiguity': ('', configure_analyse_ambiguity_parser),
    'convert': ('', configure_convert_parser)
}
