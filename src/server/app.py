import os
import uvicorn
from fastapi import FastAPI

from core.utils import read_yaml
from routers import (
    blockchain_router,
)


class Server:
    """class to handle API server"""
    def __init__(self):
        self.app = FastAPI()
        self.host = None
        self.port = None
        self._prepare()
        self._import_routers()

    def serve(self, host: str = None, port: int = None):
        print("serving")

        if host is None:
            host = self.host
        if port is None:
            port = self.port
        uvicorn.run(self.app, host=host, port=port, log_level="info")

    def _import_routers(self):
        self.app.include_router(blockchain_router, tags=["Blockchain Query"], prefix="")

    def _prepare(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        cnf = read_yaml(__location__ + "/config/config.yaml")
        self.host = cnf["APP_HOST"]
        self.port = cnf["APP_PORT"]
