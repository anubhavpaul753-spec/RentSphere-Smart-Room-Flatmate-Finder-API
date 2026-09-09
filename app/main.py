from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import user, auth, room

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


@app.get("/")
def root():
    return {
        "message": "Welcome to RentSphere API 🏠",
        "status": "online",
        "docs": "/docs"
    }
