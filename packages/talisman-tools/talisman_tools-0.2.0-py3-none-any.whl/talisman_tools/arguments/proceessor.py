from argparse import ArgumentParser, Namespace
from pathlib import Path

from tp_interfaces.abstract import AbstractDocumentProcessor


def get_processor_factory(parser: ArgumentParser):
    argument_group = parser.add_argument_group(title='Model arguments')
    argument_group.add_argument('-model_paths', nargs='+', type=Path, metavar='<model path>', required=True,
                                help='Paths to configuration files or serialized models')
    argument_group.add_argument('--wrapper', type=Path, metavar='<wrapper path>', help='Path to wrapper configuration file', default=None)

    def get_processor(args: Namespace) -> AbstractDocumentProcessor:
        from talisman_tools.configure import load_or_configure, wrap_model
        from tp_interfaces.helpers.io import read_json

        processor = load_or_configure(args.model_paths)
        if args.wrapper is not None:
            processor = wrap_model(processor, read_json(args.wrapper))
        return processor

    return get_processor
