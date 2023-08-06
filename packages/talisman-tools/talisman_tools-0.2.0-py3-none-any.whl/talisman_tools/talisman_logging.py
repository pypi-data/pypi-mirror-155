import logging

from jsonformatter import JsonFormatter


def create_json_formatter() -> JsonFormatter:
    return JsonFormatter(
        fmt={"level": "levelname", "msg": "message", "time": "asctime"},
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        mix_extra=True,
        skipkeys=True,
        ensure_ascii=False,
        default=lambda o: "NON-SERIALIZABLE"
    )


def configure_json_logging(level=logging.INFO):
    stderr_handler = logging.StreamHandler()
    json_formatter = create_json_formatter()
    stderr_handler.setFormatter(json_formatter)
    logging.basicConfig(level=level, handlers=[stderr_handler])
