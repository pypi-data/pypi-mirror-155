from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Callable

from talisman_tools.arguments.reader import get_reader_factory
from talisman_tools.commands.model.commands.evaluate.action import mode  # TODO: pulling unused dependencies
from tp_interfaces.abstract import AbstractDocumentProcessor


def configure_evaluate_parser(parser: ArgumentParser, extra_actions: Callable[[Namespace], None]) -> None:
    parser.add_argument('eval_mode', type=str, choices=set(mode), metavar='<evaluation mode>')
    parser.add_argument('--config', type=Path, metavar='<document processing config path>')

    reader_factory = get_reader_factory(parser)

    def get_action() -> Callable[[AbstractDocumentProcessor, Namespace], None]:
        def action(processor: AbstractDocumentProcessor, args: Namespace) -> None:
            from .action import evaluate
            extra_actions(args)
            evaluate(processor, args.eval_mode, reader_factory(args), args.config)

        return action

    parser.set_defaults(processor_action=get_action)
