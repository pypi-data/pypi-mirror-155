from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Callable

from tp_interfaces.abstract import AbstractDocumentProcessor


def configure_configure_parser(parser: ArgumentParser, extra_actions: Callable[[Namespace], None]) -> None:
    parser.add_argument('out_path', type=Path, metavar='<model out path>')

    def get_action() -> Callable[[AbstractDocumentProcessor, Namespace], None]:
        def action(processor: AbstractDocumentProcessor, args: Namespace) -> None:
            extra_actions(args)
            processor.save(args.out_path)
            print(f"Saved {processor} model")

        return action

    parser.set_defaults(processor_action=get_action)
