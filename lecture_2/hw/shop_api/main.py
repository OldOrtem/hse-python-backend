from fastapi import FastAPI
from .api.routes import cartRouter, itemRouter
from prometheus_fastapi_instrumentator import Instrumentator
app = FastAPI(title="Shop API")
Instrumentator().instrument(app).expose(app)
app.include_router(cartRouter)
app.include_router(itemRouter)