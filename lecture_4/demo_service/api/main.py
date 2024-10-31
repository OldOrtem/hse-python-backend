from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from . import users, utils


def create_app():
    _app = FastAPI(
        title="Testing Demo Service",
        lifespan=utils.initialize,
    )

    _app.add_exception_handler(ValueError, utils.value_error_handler)
    _app.include_router(users.router)
    Instrumentator().instrument(_app).expose(_app)
    return _app


app = create_app()