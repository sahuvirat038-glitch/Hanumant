from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.routers.users import router as users_router
from app.routers.categories import router as category_router
from app.routers.units import router as units_router
from app.routers.businesses import router as business_router
from app.routers.retailers import router as retailers_router
from app.routers.products import router as products_router



app = FastAPI(
    title=settings.APP_NAME,
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(category_router)
app.include_router(units_router)
app.include_router(business_router)
app.include_router(retailers_router)
app.include_router(products_router)



@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}"}