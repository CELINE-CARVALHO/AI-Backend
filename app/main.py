from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================
load_dotenv()

# =========================
# DATABASE
# =========================
from app.database import Base, engine

# =========================
# ROUTERS
# =========================
from app.routes import auth
from app.routes.google_oauth import router as google_oauth_router

from app.api.routes import (
    emails,
    tasks,
    calendar,
    dashboard as dashboard_api,
)

# =========================
# CREATE DATABASE TABLES
# =========================
# This runs ONCE at startup
# Creates tables like oauth_tokens if missing
Base.metadata.create_all(bind=engine)

# =========================
# FASTAPI APP
# =========================
app = FastAPI(
    title="AI Executive Secretary API",
    version="1.0.0",
)

# =========================
# CORS CONFIG
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # React / Vite frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# AUTH ROUTES
# =========================
# Internal auth (JWT, user identity)
app.include_router(auth.router, tags=["Auth"])

# Google OAuth (Gmail permission flow)
# Enables:
#   /auth/google/login
#   /auth/google/callback
app.include_router(google_oauth_router, tags=["Google OAuth"])

# =========================
# API ROUTES (PROTECTED)
# =========================
app.include_router(emails.router, prefix="/emails", tags=["Emails"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(calendar.router, prefix="/calendar", tags=["Calendar"])
app.include_router(dashboard_api.router, prefix="/dashboard", tags=["Dashboard"])

# =========================
# HEALTH CHECKS
# =========================
@app.get("/", tags=["Health"])
def root():
    return {"status": "running"}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
