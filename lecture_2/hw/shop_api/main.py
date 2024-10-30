from fastapi import FastAPI

from lecture_2.hw.shop_api.api.routes import cartRouter, itemRouter
app = FastAPI(title="Shop API")

app.include_router(cartRouter)
app.include_router(itemRouter)

