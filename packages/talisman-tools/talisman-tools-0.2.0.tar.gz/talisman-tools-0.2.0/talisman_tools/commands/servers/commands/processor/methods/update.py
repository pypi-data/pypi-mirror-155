import logging
from logging import Logger
from typing import List, Type

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder

from talisman_tools.commands.servers.server_helper import log_debug_data
from tp_interfaces.abstract import AbstractUpdatableModel, AbstractUpdate

_logger = logging.getLogger(__name__)


def register_update(app: FastAPI, model: AbstractUpdatableModel, input_type: Type[AbstractUpdate], logger: Logger = _logger):
    @app.post("/update/")
    async def update(request: Request, *, update_model: input_type):
        log_debug_data(logger, "update requested", request, update=update_model)
        try:
            model.update(update_model)
            log_debug_data(logger, "successfull update", request, update=update_model)
        except Exception as e:
            logger.error("error during update", exc_info=e, extra={"update": jsonable_encoder(update_model)})
            raise HTTPException(status_code=400, detail=str(e))


def register_info(app: FastAPI, model: AbstractUpdatableModel, input_type: Type[AbstractUpdate], logger: Logger = _logger):
    @app.get("/info/", response_model=List[input_type], response_model_exclude={'mode'})
    async def info(request: Request):
        log_debug_data(logger, "requested info", request)
        return model.info()
