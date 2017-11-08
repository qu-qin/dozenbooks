from webapp2 import Route
from webapp2_extras.routes import PathPrefixRoute

# handler
from handlers.spa import SPAHandler
from handlers.vdisk import VdiskHandler
from workers.sender import SenderTask

# api handlers
from endpoints.search import SearchHandler
from endpoints.send import SendHandler

_ROUTES = [
    # oauth providers
    PathPrefixRoute("/providers", [
        Route("/vdisk", handler=VdiskHandler, name="provider_vdisk")
    ]),
    # apis
    PathPrefixRoute("/api", [
        Route("/search", handler=SearchHandler, name="api_search"),
        Route("/send", handler=SendHandler, name="api_send"),
    ]),
    # tasks
    PathPrefixRoute("/tasks", [
        Route("/sender", handler=SenderTask, name="tasks_sender")
    ]),
    Route("/", handler=SPAHandler, name="spa_main")
]


def get_routes():
    return _ROUTES


def add_routes(app):
    for r in _ROUTES:
        app.router.add(r)
