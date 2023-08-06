from talisman_tools.configure import configure_model
from tp_interfaces.abstract import AbstractDocumentProcessor


def wrap_model_action(config: dict) -> AbstractDocumentProcessor:
    """
    create model from config and wraps it with respect to specified wrapper and wrapper configuration
    :param config: dict with required "wrapper" and "to_wrap" keys. Optional "plugin" and "config" keys are taken into account
    :return: wrapped document processor
    """
    from talisman_tools.plugin import WrapperPlugins  # inline import to avoid circular imports
    if isinstance(config["wrapper"], dict):
        plugin = config["wrapper"].get("plugin")
        model = config["wrapper"]["model"]
    elif isinstance(config["wrapper"], str):
        plugin = None
        model = config["wrapper"]
    else:
        raise ValueError
    try:
        wrapper_factory = WrapperPlugins.plugins[plugin][model]
        return wrapper_factory.from_config(configure_model(config['to_wrap']), config.get("config", {}))
    except ValueError:
        raise ValueError(f"{config['wrapper']} is not found in {config.get('plugin') or 'default'} plugin")


def configure_model_action(config: dict) -> AbstractDocumentProcessor:
    """
    create model from config
    :param config: dict with required "model" key
    :return: configured model
    """
    return configure_model(config)
