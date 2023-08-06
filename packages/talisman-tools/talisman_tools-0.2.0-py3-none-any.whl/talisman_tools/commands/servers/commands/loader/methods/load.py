import logging
from logging import Logger
from typing import Dict, List

from fastapi import FastAPI, HTTPException, Request
from tdm.json_schema import TalismanDocumentModel

from talisman_tools.commands.servers.server_helper import log_debug_data
from tp_interfaces.knowledge_base.interfaces import DisambiguationKB

_logger = logging.getLogger(__name__)


def register_load_docs(
        app: FastAPI,
        kb: DisambiguationKB,
        logger: Logger = _logger
):
    @app.post('/', response_model=List[Dict[str, str]])
    async def load_docs(request: Request, *, docs: List[TalismanDocumentModel]):
        log_debug_data(logger, f"got {len(docs)} documents for loading", request, messages=docs)

        input_docs = tuple(it.to_doc() for it in docs)
        status = kb.bind_facts_and_load_docs(input_docs)

        logger.info(f'Loading info', extra={'info': status})

        if all(status_ == 'failed' for status_ in map(lambda info: info['status'], status)):
            return HTTPException(status_code=500, detail='No document was loaded')
        return status
