from frontend.app import app
from frontend.routers import router as tms_router
from frontend.routers.products import router as products_router

app.include_router(products_router)
app.include_router(tms_router)
