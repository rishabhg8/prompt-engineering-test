from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import problems, evaluate, scenarios, mcqs

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="FastAPI Core Backend Engine and Task Scenario Bank for AIMap (Algomap for AI Interviews)",
)

# Configure CORS Middleware for frontend integration (Streamlit, React, Vue, Next.js, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(problems.router)
app.include_router(evaluate.router)
app.include_router(scenarios.router)
app.include_router(mcqs.router)


@app.get("/", summary="Root API Info")
def root():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "mock_mode": getattr(settings, "MOCK_MODE", True),
        "documentation": "/docs",
        "endpoints": [
            "/health",
            "/api/health",
            "/api/scenarios",
            "/api/scenarios/{id}",
            "/api/evaluate/guardrails",
            "/api/mcqs",
            "/api/mcqs/{id}",
            "/api/problems",
            "/api/evaluate",
        ],
    }


@app.get("/health", summary="Health Check")
@app.get("/api/health", summary="API Health Check")
def health_check():
    return {
        "status": "healthy",
        "mock_mode": getattr(settings, "MOCK_MODE", True),
        "version": settings.VERSION,
        "models_supported": getattr(settings, "SMALL_MODELS", []),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
