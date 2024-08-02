from typing import Protocol
from fastapi import FastAPI
from starlette.types import ASGIApp

from adapters.rest.v1 import router as v1_router
from config.dependencies import database


class ASGIAppFactory(Protocol):
    def create(self) -> ASGIApp: ...


class FastApiAppFactory(ASGIAppFactory):
    def create(self) -> ASGIApp:
        app = FastAPI(lifespan=self._lifespan)
        app.include_router(v1_router)
        return app

    async def _lifespan(self, app: FastAPI):
        yield
        await database.close()
