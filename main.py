import uvicorn
from app.setup import create_app
from config.config import settings
import os

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.APP_PORT,
        reload=settings.ENV != "production"
    )
