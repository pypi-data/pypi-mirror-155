from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Callable

from talisman_tools.arguments.reader import get_reader_factory
from talisman_tools.arguments.serializer import get_serializer_factory
from tp_interfaces.abstract import AbstractDocumentProcessor


def configure_process_parser(parser: ArgumentParser, extra_actions: Callable[[Namespace], None]) -> None:
    reader_factory = get_reader_factory(parser)
    serializer_factory = get_serializer_factory(parser)

    parser.add_argument('--config', type=Path, metavar='<document processing config path>')
    parser.add_argument('--batch', type=int, metavar='<batch size>', default=1000)

    def get_action() -> Callable[[AbstractDocumentProcessor, Namespace], None]:
        def action(processor: AbstractDocumentProcessor, args: Namespace) -> None:
            from tp_interfaces.helpers.io import read_json

            extra_actions(args)
            reader = reader_factory(args)
            serializer = serializer_factory(args)

            with processor:
                processor_config_type = processor.config_type
                config = processor_config_type.parse_obj(read_json(args.config)) if args.config else processor_config_type()
                serializer(processor.process_stream(reader.read(), config, args.batch))

        return action

    parser.set_defaults(processor_action=get_action)
