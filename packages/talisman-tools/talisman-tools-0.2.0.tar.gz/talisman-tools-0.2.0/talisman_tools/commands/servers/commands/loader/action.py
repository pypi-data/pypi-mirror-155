import logging
from argparse import Namespace

from fastapi import FastAPI

from talisman_tools.commands.servers.commands.loader.methods.load import register_load_docs
from talisman_tools.commands.servers.server_helper import register_exception_handlers, register_shutdown
from tp_interfaces.knowledge_base.manager import KBManager


logger = logging.getLogger(__name__)


def action(args: Namespace) -> FastAPI:
    app = FastAPI(title='kb loader server', description='kb loader server')

    kb = KBManager().knowledge_base

    register_load_docs(
        app=app,
        kb=kb,
        logger=logger
    )

    register_exception_handlers(app)
    register_shutdown(app, kb)

    kb.__enter__()
    return app
