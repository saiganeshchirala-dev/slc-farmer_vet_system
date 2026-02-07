from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.database import engine, Base
from .api.v1.endpoints import auth, users, animals
from .core.config import settings

# Create Database Tables
Base.metadata.create_all(bind=engine)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(animals.router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    from .db.database import engine
    from sqlalchemy import text
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        db_status = "Connected"
    except Exception as e:
        db_status = f"Disconnected: {str(e)}"
    
    db_type = "PostgreSQL" if "postgres" in str(engine.url) else "SQLite"
    
    return {
        "status": "Healthy",
        "database": {
            "type": db_type,
            "connection": db_status
        }
    }


# --- Static Files & Frontend Routes ---
# Define frontend directory
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../public"))

# Serve cleanup URLs (e.g. /signup -> signup.html)
@app.get("/signup")
async def read_signup():
    if os.path.exists(os.path.join(frontend_dir, "signup.html")):
        return FileResponse(os.path.join(frontend_dir, "signup.html"))
    return {"error": "File not found"}

@app.get("/otp")
async def read_otp():
    if os.path.exists(os.path.join(frontend_dir, "otp.html")):
        return FileResponse(os.path.join(frontend_dir, "otp.html"))
    return {"error": "File not found"}

# Mount Static Files (Catch-all for other files)
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
# --- End Static Files ---
