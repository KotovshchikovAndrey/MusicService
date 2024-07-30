import uvicorn
from config.app import create_app
from config.settings import settings


app = create_app()


def run_server() -> None:
    uvicorn.run(
        "index:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.is_debug,
    )
