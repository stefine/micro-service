from fastapi import FastAPI
from pathlib import Path
import yaml


def create_server(register_repo=None, register_service=None):
    server = FastAPI(debug=True)
    oas_doc = yaml.safe_load((Path(__file__).parent/"oas.yaml").read_text())
    server.openapi = lambda: oas_doc
    server.register_repo = register_repo
    server.register_serv = register_service
    return server
