# backend/app/main.py
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import logging

from app.config import Settings
from app.routers import complaints, tracking, escalation
from app.services.db_service import init_db

settings = Settings()

logger = logging.getLogger("uvicorn.access")

app = FastAPI(
    title="CyberSathi Backend",
    version="0.1.0",
    description="Backend API for CyberSathi (WhatsApp chatbot for Cybercrime Helpline 1930)."
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else [settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    print("Initializing database...")
    init_db()
    print("Database initialized successfully")

# include routers
app.include_router(complaints.router, prefix="/api/v1/complaints", tags=["complaints"])
app.include_router(tracking.router, prefix="/api/v1/tracking", tags=["tracking"])
app.include_router(escalation.router, prefix="/api/v1/escalation", tags=["escalation"])

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "service": "CyberSathi Backend"}

@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=settings.PORT, reload=settings.DEBUG)