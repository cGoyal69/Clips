
from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics
from app.api.routes import clips
from app.core.config import settings
from app.db.models import Base
from app.core.database import engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    debug=settings.DEBUG
)

# Add Prometheus middleware for metrics
app.add_middleware(
    PrometheusMiddleware,
    app_name="sound_clip_api",
    group_paths=True,
    prefix="sound_clip_api",
)

# Add metrics endpoint for Prometheus
app.add_route("/metrics", handle_metrics)

# Include routers
app.include_router(clips.router, prefix=settings.API_PREFIX)

@app.get("/")
def read_root():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": settings.DESCRIPTION
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)