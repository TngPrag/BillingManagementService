import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE
from starlette.responses import JSONResponse

from routers.bill_route import bill_routes
from routers.user_route import user_routes
from fs.fs import fs_open, Base, engine,create_tables
from logic.core.user_model import init_admin_user
from config.config import settings

import os


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Dynamic CORS origins
ALLOWED_ORIGINS = [
    "https://bill-management.com",  # Trusted frontend
    "http://localhost:3000"
]

def create_app() -> FastAPI:
    create_tables()
    app = FastAPI(
        title="Auth & User API",
        version="0.1.0",
        docs_url="/docs" if not is_production() else None,
        redoc_url=None,
    )

    # CORS setup
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )



    # Shutdown hook
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Service shutdown initiated.")

    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        try:
            #fs_open()  # Or replace with lightweight health logic
            return {"status": "ok"}
        except Exception:
            return JSONResponse(
                content={"status": "unhealthy"},
                status_code=HTTP_503_SERVICE_UNAVAILABLE
            )

    # Register routers
    app.include_router(user_routes)
    app.include_router(bill_routes)

    return app


def is_production() -> bool:
    return os.getenv("ENV", "development").lower() == "production"

def run_setup():
    try:
        # Ensure tables are created first
        #Base.metadata.create_all(bind=engine)
        create_tables()
        db = fs_open()

        #Then init the admin
        result = init_admin_user(db)
        if result and not result.success:
            logger.error(f"Admin initialization failed: {result.error}")
        else:
            logger.info("Admin user initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize admin user: {e}")
    finally:
        try:
            db.close()
        except Exception:
            pass
