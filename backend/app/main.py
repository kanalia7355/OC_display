from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import logging
from dotenv import load_dotenv

from .routers import depth, processing
from .config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

load_dotenv()

# Debug port environment variable
port_env = os.getenv("PORT")
print(f"🔍 PORT environment variable: {port_env}")
print(f"🔍 All environment variables containing 'PORT': {[k for k in os.environ.keys() if 'PORT' in k.upper()]}")

app = FastAPI(
    title="Depth Estimation API",
    description="API for depth estimation and 3D visualization",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(depth.router, prefix="/api/depth", tags=["depth"])
app.include_router(processing.router, prefix="/api/processing", tags=["processing"])

# Add static file serving for temporary files
if os.path.exists(settings.TEMP_DIR):
    app.mount("/temp", StaticFiles(directory=settings.TEMP_DIR), name="temp")

@app.get("/")
async def root():
    return {
        "message": "Depth Estimation API",
        "version": "1.0.0",
        "status": "running",
        "port": os.getenv("PORT", "not set"),
        "environment": settings.ENVIRONMENT
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "port": os.getenv("PORT", "not set"),
        "host": "0.0.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENVIRONMENT") == "development"
    )
    print(f"Server starting on port {port}")