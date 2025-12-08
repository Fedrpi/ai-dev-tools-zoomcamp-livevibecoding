"""
LiveCoding Interview API

FastAPI application for conducting live coding interviews with real-time synchronization.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI application
app = FastAPI(
    title="LiveCoding Interview API",
    description="""
    REST API for LiveCoding Interview platform.
    This API enables real-time coding interviews with live code synchronization
    between interviewer and candidate.
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
    },
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS for Frontend
# In development, allow localhost:5173 (Vite dev server)
# In production, update with actual frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root endpoint - API status check
    """
    return {
        "message": "Welcome to LiveCoding Interview API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {"status": "healthy"}


# Import API routes
from app.api.routes import auth, evaluations, problems, sessions, ws

# Register routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(problems.router, prefix="/api/problems", tags=["Problems"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["Sessions"])
app.include_router(evaluations.router, prefix="/api/sessions", tags=["Evaluations"])
app.include_router(ws.router, prefix="/api", tags=["WebSocket"])
