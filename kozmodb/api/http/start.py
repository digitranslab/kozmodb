import gc

gc.disable()

from flask import Flask

from kozmodb.api.http.initialize import initialize_app
from kozmodb.interfaces.storage import db
from kozmodb.utilities import log
from kozmodb.utilities.config import config
from kozmodb.utilities.functions import init_lexer_parsers
from kozmodb.integrations.libs.ml_exec_base import process_cache
from kozmodb.api.common.middleware import PATAuthMiddleware


from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.middleware.wsgi import WSGIMiddleware
import uvicorn

from kozmodb.api.a2a import get_a2a_app
from kozmodb.api.mcp import get_mcp_app

gc.enable()

logger = log.getLogger(__name__)


def start(verbose, app: Flask = None):
    db.init()
    init_lexer_parsers()

    if app is None:
        app = initialize_app()

    port = config["api"]["http"]["port"]
    host = config["api"]["http"]["host"]

    process_cache.init()

    routes = []
    # Specific mounts FIRST
    a2a = get_a2a_app()
    a2a.add_middleware(PATAuthMiddleware)
    mcp = get_mcp_app()
    mcp.add_middleware(PATAuthMiddleware)
    routes.append(Mount("/a2a", app=a2a))
    routes.append(Mount("/mcp", app=mcp))

    # Root app LAST so it won't shadow the others
    routes.append(Mount("/", app=WSGIMiddleware(app)))

    # Setting logging to None makes uvicorn use the existing logging configuration
    uvicorn.run(Starlette(routes=routes, debug=verbose), host=host, port=int(port), log_level=None, log_config=None)
