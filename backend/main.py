from fastapi import FastAPI
from routes.routes import router

app = FastAPI(title="URL Shortener API")

# Include the main router
app.include_router(router)
