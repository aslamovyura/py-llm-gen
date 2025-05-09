from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.infrastructure.di.container import container
from .routes.client import router as client_router
from .routes.user import router as user_router
from .routes.offer import router as offer_router
from .routes.request import router as request_router
from .routes.equipment import router as equipment_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await container.init()
    yield
    # Shutdown
    await container.cleanup()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Database Search API",
        description="Clean Architecture API for Database Search",
        version="1.0.0",
        lifespan=lifespan
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(client_router)
    app.include_router(user_router)
    app.include_router(offer_router)
    app.include_router(request_router)
    app.include_router(equipment_router)

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app

# app = create_app() 