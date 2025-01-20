import asyncio

from frontend.app import app
from frontend.routers.products import router as products_router
from frontend.routers import router as tms_router
from frontend.db import Base, engine

@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
app.include_router(products_router)
app.include_router(tms_router)
