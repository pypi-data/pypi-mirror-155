import time
from argparse import Namespace
from typing import Tuple

from tdm.datamodel import TalismanDocument

from tp_interfaces.abstract import AbstractDocumentProcessor


def _get_time(docs: Tuple[TalismanDocument], model: AbstractDocumentProcessor):
    start_time = time.time()
    config_type = model.config_type
    model.process_docs(docs, config_type())
    end_time = time.time()

    return end_time - start_time


def measure_time(docs: Tuple[TalismanDocument], model: AbstractDocumentProcessor, count: int):
    print('Time:')
    average_time = 0

    for _ in range(count):
        current_time = _get_time(docs, model)
        average_time += current_time
        print(f'\t{current_time}')

    average_time /= count
    print(f'Average: {average_time}\n')


def action(args: Namespace):
    docs = args.reader.read()
    count = args.count
    processor = args.model

    with processor:
        measure_time(docs, processor, count)
