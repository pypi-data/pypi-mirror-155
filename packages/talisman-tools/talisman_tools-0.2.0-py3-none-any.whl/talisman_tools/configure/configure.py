import json
import logging
from itertools import groupby
from os import PathLike
from pathlib import Path
from pickle import PickleError
from typing import Callable, Dict, FrozenSet, Iterable, List, Union

from tp_interfaces.abstract import AbstractDocumentProcessor, AbstractMultipleConfigConstructableModel
from tp_interfaces.processors.composite import SequentialDocumentProcessor

ActionsType = Dict[FrozenSet[str], Callable[[dict], AbstractDocumentProcessor]]


_logger = logging.getLogger(__name__)


def _process_config(config: dict) -> AbstractDocumentProcessor:
    from talisman_tools.plugin import WrapperActionsPlugins

    plugin = config.get("plugin")
    actions = WrapperActionsPlugins.plugins[plugin]

    proper_actions = [action for required_key_set, action in actions.items() if required_key_set <= set(config.keys())]
    if len(proper_actions) > 1:
        raise Exception("Provided config can be processed by multiple actions")
    if len(proper_actions) == 0:
        raise Exception("Provided config can not be processed by any action")

    action, = proper_actions
    return action(config)


def wrap_model_from_config(config: Union[List[dict], dict]) -> AbstractDocumentProcessor:
    if isinstance(config, list) and len(config) == 1:
        config = config[0]
    if isinstance(config, dict):
        return _process_config(config)
    if isinstance(config, list):
        if len(config) == 0:
            raise Exception("Provided list config has no elements")
        return SequentialDocumentProcessor(map(_process_config, config))
    else:
        raise Exception("Provided config contains neither list, nor dict")


def configure_model(config: Union[List[dict], dict]) -> AbstractDocumentProcessor:
    from talisman_tools.plugin import ProcessorPlugins  # inline import to avoid circular imports
    if isinstance(config, list) and len(config) == 1:
        config = config[0]
    if isinstance(config, dict):  # build model from config
        if config.get("plugin") is None and config["model"] == "wrapper":
            return wrap_model_from_config(config["config"])
        return ProcessorPlugins.plugins[config["plugin"]][config["model"]].from_config(config.get("config", {}))
    if isinstance(config, list):
        if len(config) == 0:
            raise Exception("Couldn't configure empty list model")
        key = lambda c: (c.get("plugin", ''), c["model"])
        groupped = {k: tuple(v) for k, v in groupby(config, key=key)}

        models = []

        for (plugin, model), cfgs in groupped.items():
            if plugin == '' and model == "wrapper":
                for cfg in cfgs:
                    models.append(configure_model(cfg))
                continue
            type_ = ProcessorPlugins.plugins[plugin][model]
            if issubclass(type_, AbstractMultipleConfigConstructableModel):
                models.append(type_.from_configs([cfg.get("config", {}) for cfg in cfgs]))
            else:
                for cfg in cfgs:
                    models.append(type_.from_config(cfg.get("config", {})))

        if len(models) == 1:
            return models[0]
        return SequentialDocumentProcessor(models)


def load_or_configure(model_or_config_paths: Iterable[Union[str, PathLike]]) -> AbstractDocumentProcessor:
    def load_as_model(model_path: Path) -> AbstractDocumentProcessor:
        return AbstractDocumentProcessor.load(model_path)

    def load_as_config(config_path: Path) -> AbstractDocumentProcessor:
        config = read_json_config(config_path)
        return configure_model(config)

    def convert_to_model(model_or_config_path: Path) -> AbstractDocumentProcessor:
        if model_or_config_path.suffix == '.json':
            return load_as_config(model_or_config_path)

        if model_or_config_path.suffix == '.pkl':
            return load_as_model(model_or_config_path)

        _logger.warning(f'Unrecognized filename extension for {model_or_config_path}')

        try:
            return load_as_config(model_or_config_path)
        except ValueError:
            pass

        try:
            return load_as_model(model_or_config_path)
        except PickleError:
            pass

        raise ValueError(f'Unable to read {model_or_config_path} neither as model configuration file nor as serialized model file!')

    models = tuple(map(convert_to_model, map(Path, model_or_config_paths)))

    if not models:
        raise ValueError("Neither model paths nor model configs were provided")
    if len(models) == 1:
        return models[0]
    return SequentialDocumentProcessor(models)  # here we could get `Composite(Composite(...), Composite(...))`


def read_json_config(path: Union[str, Path]):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
