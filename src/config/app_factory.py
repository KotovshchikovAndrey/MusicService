from contextlib import asynccontextmanager
from typing import Protocol

from fastapi import FastAPI
from starlette.types import ASGIApp

from adapters.driven.sql.connection import SqlDatabaseConnection
from adapters.driving.graphql import router as graphql_router
from adapters.driving.rest.v1 import router as v1_router
from config.ioc_container import container


class ASGIAppFactory(Protocol):
    def create(self) -> ASGIApp: ...


class FastApiAppFactory(ASGIAppFactory):
    def create(self) -> ASGIApp:
        app = FastAPI(lifespan=self._lifespan)
        app.include_router(v1_router)
        app.include_router(graphql_router)
        return app

    @asynccontextmanager
    async def _lifespan(self, app: FastAPI):
        database = container.resolve(SqlDatabaseConnection)
        yield
        await database.close()
