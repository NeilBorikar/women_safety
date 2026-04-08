from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

# 🔌 DB
from app.db.mongodb import connect_to_mongo, close_mongo_connection

# 📦 Routes
from app.routes import (
    auth_routes,
    user_routes,
    alert_routes,
    location_routes,
    evidence_routes,
    notification_routes
)

# ⚙️ Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# 🔁 Lifespan Manager (modern FastAPI way)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🚀 Startup
    logger.info("🚀 Starting Women Safety Backend...")
    await connect_to_mongo()

    yield

    # 🛑 Shutdown
    logger.info("🛑 Shutting down Women Safety Backend...")
    await close_mongo_connection()


from fastapi.middleware.cors import CORSMiddleware

# 🚀 App Initialization
app = FastAPI(
    title="Women Safety Backend 🚨",
    description="AI-Powered Emergency Response & Safety System",
    version="1.0.0",
    lifespan=lifespan
)

# 🌐 CORS Config for React Native / ESP32 Hardware integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 🌐 Root Health Check
@app.get("/", methods=["GET", "HEAD"])
async def root():
    return {
        "status": "running",
        "message": "Women Safety Backend is live 🚨",
        "version": "1.0.0"
    }


# ❤️ Health Check Endpoint (IMPORTANT FOR DEPLOYMENT)
@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }


# 🔐 AUTH ROUTES
app.include_router(
    auth_routes.router,
    prefix="/auth",
    tags=["Authentication"]
)

# 👤 USER ROUTES
app.include_router(
    user_routes.router,
    prefix="/user",
    tags=["User"]
)

# 🚨 ALERT ROUTES
app.include_router(
    alert_routes.router,
    prefix="/alert",
    tags=["Alert"]
)

# 📍 LOCATION ROUTES
app.include_router(
    location_routes.router,
    prefix="/location",
    tags=["Location"]
)

# 🎥 EVIDENCE ROUTES
app.include_router(
    evidence_routes.router,
    prefix="/evidence",
    tags=["Evidence"]
)

# 🔔 NOTIFICATION ROUTES
app.include_router(
    notification_routes.router,
    prefix="/notification",
    tags=["Notification"]
)


# ⚠️ GLOBAL EXCEPTION HANDLER (OPTIONAL UPGRADE)
from fastapi.responses import JSONResponse
from fastapi import Request
from app.utils.exceptions import AppException


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail
        }
    )


# ⚠️ FALLBACK ERROR HANDLER
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Error: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error"
        }
    )