import logging
from contextlib import asynccontextmanager
from logging.config import dictConfig
from typing import Protocol

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp

from adapters.driven.sql.connection import SQLDatabaseConnection
from adapters.driving.graphql import router as graphql_router
from adapters.driving.rest.v1 import router as v1_router
from config.ioc_container import container
from config.logger import LoggerConfig
from domain.errors.base import DomainError


class ASGIAppFactory(Protocol):
    def create(self) -> ASGIApp: ...


class FastApiAppFactory(ASGIAppFactory):
    def create(self) -> ASGIApp:
        dictConfig(LoggerConfig().model_dump())
        container.init()

        app = FastAPI(lifespan=self._lifespan)
        app.include_router(v1_router)
        app.include_router(graphql_router)

        app.add_exception_handler(RequestValidationError, self._handle_request_exception)
        app.add_exception_handler(DomainError, self._handle_domain_exception)
        app.add_exception_handler(Exception, self._handle_internal_exception)

        return app

    @asynccontextmanager
    async def _lifespan(self, _: FastAPI):
        database = container.resolve(SQLDatabaseConnection)
        logging.info("Server was running")

        yield

        await database.close()
        logging.info("Server was closed")

    def _handle_request_exception(self, _: Request, exc: RequestValidationError) -> None:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"message": exc.errors()}),
        )

    def _handle_domain_exception(
        self,
        _: Request,
        exc: DomainError,
    ) -> None:
        return JSONResponse(
            status_code=exc.code,
            content={"message": exc.message},
        )

    def _handle_internal_exception(self, _: Request, exc: Exception) -> None:
        # TODO: log exc
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error occured"},
        )
