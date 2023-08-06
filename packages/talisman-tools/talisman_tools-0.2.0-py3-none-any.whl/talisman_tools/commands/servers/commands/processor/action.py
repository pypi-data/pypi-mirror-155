import logging
from argparse import Namespace
from typing import Callable

from fastapi import FastAPI

from talisman_tools.commands.servers.commands.processor.methods.process import register_process_docs
from talisman_tools.commands.servers.commands.processor.methods.update import register_info, register_update
from talisman_tools.commands.servers.server_helper import register_exception_handlers, register_shutdown
from talisman_tools.plugin import EndpointPlugins, TDMPlugins
from tp_interfaces.abstract import AbstractDocumentProcessor, AbstractUpdatableModel

logger = logging.getLogger(__name__)


def action(args: Namespace, processor_factory: Callable[[Namespace], AbstractDocumentProcessor]) -> FastAPI:
    document_model = TDMPlugins.plugins[args.dm]

    processor = processor_factory(args)
    logger.info(f"Loaded {processor}")

    app = FastAPI(title="talisman-ie REST server", description=f"talisman-ie REST server for {processor}")

    register_process_docs(
        app=app,
        endpoint='/',
        processor=processor,
        document_model=document_model,
        logger=logger
    )

    if isinstance(processor, AbstractUpdatableModel):
        register_update(app, processor, processor.update_type)
        register_info(app, processor, processor.update_type)

    for endpoint, register in EndpointPlugins.flattened.items():
        register()(app=app, endpoint=endpoint, processor=processor, logger=logger)

    register_exception_handlers(app, logger=logger)
    register_shutdown(app, processor)

    processor.__enter__()
    return app
