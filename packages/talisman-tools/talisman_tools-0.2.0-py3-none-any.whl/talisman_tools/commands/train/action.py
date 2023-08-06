from argparse import Namespace
from pathlib import Path
from typing import Optional, Tuple

from tdm.datamodel import TalismanDocument

from talisman_tools.configure import read_json_config
from talisman_tools.plugin import TrainerPlugins
from tp_interfaces.readers.abstract import AbstractReader


def _read_docs(reader: Optional[AbstractReader]) -> Optional[Tuple[TalismanDocument, ...]]:
    if reader is None:
        return None
    return tuple(reader.read())


def train(train_reader: AbstractReader, dev_reader: Optional[AbstractReader], args: Namespace):
    train_docs = tuple(train_reader.read())
    dev_docs = _read_docs(dev_reader)
    config = read_json_config(args.config_path)

    trainer = TrainerPlugins.plugins[config['plugin']][config['model']](config['config'])

    trained_model = trainer.train(train_docs, dev_docs)
    trained_model.save(Path(args.out_model_path))
