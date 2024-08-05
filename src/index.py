import uvicorn

from config.app_factory import FastApiAppFactory
from config.settings import settings

app_factory = FastApiAppFactory()
app = app_factory.create()


def run_server() -> None:
    uvicorn.run(
        "index:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.is_debug,
    )
