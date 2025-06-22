from fastapi import APIRouter
from routes.urls import router as urls_router

# Create the main router
router = APIRouter()

router.include_router(
    urls_router,
    prefix="/url",
    tags=["URL Shortener"]
)

def register_routes(app: FastAPI):
    app.include(router)