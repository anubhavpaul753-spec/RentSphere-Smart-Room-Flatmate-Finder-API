import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .routers import user, auth, room, bookmark, review

app = FastAPI(
    title="RentSphere API",
    description="Smart Room & Flatmate Finder REST API built with FastAPI, PostgreSQL, and JWT Authentication",
    version="1.0.0"
)

# CORS configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(room.router)
app.include_router(bookmark.router)
app.include_router(review.router)

# Mount Frontend Static Assets
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.get("/")
@app.get("/app")
def serve_app():
    """
    Serve the interactive single-page application frontend directly at root
    """
    index_file = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Frontend index.html not found"}


@app.get("/api")
def root_api():
    return {
        "message": "Welcome to RentSphere API 🏠",
        "status": "online",
        "docs": "/docs",
        "app": "/"
    }

