"""
Contains the code that sets up the API.
"""
import os
from typing import Dict

from fastapi import FastAPI, status
from uvicorn import Server, Config

import fidescls
from fidescls.api import config as _acon
from fidescls.api import classify, logger as _api_logger


LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "DEBUG").upper()
logger = _api_logger.config_logger(logging_level=LOGGING_LEVEL)

app = FastAPI(title="fidescls")


def configure_routes() -> None:
    """Include all routers not defined here."""
    for router in classify.routers:
        app.include_router(router)


configure_routes()


@app.get(
    "/health",
    response_model=Dict[str, str],
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "version": "1.0.0",
                    }
                }
            }
        }
    },
    tags=["Health"],
)
async def health() -> Dict:
    "Confirm that the API is running and healthy."
    return {
        "status": "healthy",
        "version": fidescls.__version__,
    }


def start_webserver() -> None:
    """Run the webserver."""
    server = Server(Config(app, host="0.0.0.0", port=_acon.PORT))
    server.run()
