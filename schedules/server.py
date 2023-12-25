from fastapi import FastAPI
from pathlib import Path
import yaml


def create_server(repo=None, service=None):
    server = FastAPI(debug=True)
    oas_doc = yaml.safe_load((Path(__file__).parent/"oas.yaml").read_text())
    server.openapi = lambda: oas_doc
    server.register_repo = repo
    server.register_serv = service
    return server
