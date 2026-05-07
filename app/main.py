from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings

from app.routers.users import router as users_router
from app.routers.categories import router as category_router
from app.routers.units import router as units_router
from app.routers.businesses import router as business_router
from app.routers.retailers import router as retailers_router
from app.routers.products import router as products_router
from app.routers.junction import router as junction_router
from app.routers.orders import router as orders_router
from app.routers.order_items import router as order_item_router
from app.routers.payments import router as payment_router
from app.routers.invoices import router as invoices_router
from app.routers.accounting_ledger import router as ledger_router
from app.routers.conversations import router as conversations_router
from app.routers.messages import router as message_router
from app.routers.notifications import router as notifications_router
from app.routers.reviews import router as reviews_router
from app.routers.sessions import router as sessions_router
from app.routers.analytics_events import router as analytics_events_router
from app.auth.google import router as google_router
from app.routers.websockets import router as websockets_router
from app.routers.Discovery import router as discovery_router
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.middleware.rate_limit import limiter
from app.tasks.background_tasks import start_scheduler, stop_scheduler


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

@app.on_event("startup")
async def startup():
    start_scheduler()

@app.on_event("shutdown")
async def shutdown():
    stop_scheduler()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(users_router)
app.include_router(category_router)
app.include_router(units_router)
app.include_router(business_router)
app.include_router(retailers_router)
app.include_router(products_router)
app.include_router(junction_router)
app.include_router(orders_router)
app.include_router(order_item_router)
app.include_router(payment_router)
app.include_router(invoices_router)
app.include_router(ledger_router)
app.include_router(conversations_router)
app.include_router(message_router)
app.include_router(notifications_router)
app.include_router(reviews_router)
app.include_router(sessions_router)
app.include_router(analytics_events_router)
app.include_router(google_router)
app.include_router(websockets_router)
app.include_router(discovery_router)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}"}