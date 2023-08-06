from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Optional, Tuple

from talisman_tools.plugin import ReaderPlugins
from tp_interfaces.readers.abstract import AbstractReader


def get_reader_factory(parser: ArgumentParser, include_dev: bool = False):
    readers = ReaderPlugins.flattened
    argument_group = parser.add_argument_group(title="Input documents arguments")
    argument_group.add_argument('reader', metavar='<reader type>', choices=set(readers.keys()))
    argument_group.add_argument('docs_path', type=Path, metavar='<docs path>')
    if include_dev:
        argument_group.add_argument('--dev_docs_path', type=Path, metavar='<dev docs path>', default=None,
                                    help='Path to documents that will be used as development set')

        def get_reader(args: Namespace) -> Tuple[AbstractReader, Optional[AbstractReader]]:
            dev_reader = readers[args.reader](args.dev_docs_path) if args.dev_docs_path else None
            return readers[args.reader](args.docs_path), dev_reader

    else:

        def get_reader(args: Namespace) -> AbstractReader:
            return readers[args.reader](args.docs_path)

    return get_reader
