# import uvicorn
# from fastapi import FastAPI, Request, HTTPException
# from dotenv import load_dotenv
# load_dotenv() 
# app = FastAPI()
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.responses import JSONResponse
# from pydantic import ValidationError

# from app.routers import api_v1
# from app.core.limiter import init_rate_limiter, rate_limit_exception_handler
# from app.db.mongo import connect_to_mongo, close_db, get_db
# from app.middleware.auth_middleware import AuthMiddleware  # Import the JWT auth middleware

# # Routers
# from app.api.v1.admin.routes import router as admin_router
# from app.api.v1.auth.routes import router as auth_router
# from app.api.v1.github.github_auth import router as github_router
# from app.api.v1.llm.router import router as llm_router
# from app.api.v1.evaluation.router import router as eval_router
# # from app.api.v1.feedback.router import router as fb_router
# from app.api.v1.feedback.router import router as feedback_router
# from app.api.v1.analytics.router import router as analytics_router

# # Initialize the FastAPI app
# app = FastAPI(title="PromptCraft API", version="1.0")
# app.add_middleware(AuthMiddleware)

# # --- CORS Configuration ---
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://127.0.0.1:5500"],  # Frontend's origin,  # In prod, use specific origins like ['https://example.com']
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --- Middleware to Inject DB/User ---
# @app.middleware("http")
# async def inject_db_and_user(request: Request, call_next):
#     request.state.db = get_db()  # Get DB from the global state
#     # Replace with actual logic to extract user info from token
#     request.state.user_id = "64b123456789abcdef01234"  # Example user ID
#     request.state.is_admin = True  # Set admin status (replace with real logic)
#     response = await call_next(request)
#     return response

# # --- Rate Limiting Initialization ---
# @app.on_event("startup")
# async def startup_event():
#     await init_rate_limiter(app)  # Initialize rate limiting
#     await connect_to_mongo()  # Connect to MongoDB

# @app.on_event("shutdown")
# async def shutdown_event():
#     await close_db()  # Close MongoDB connection on shutdown

# # Exception handler for rate limit (429)
# app.add_exception_handler(429, rate_limit_exception_handler)

# # --- Include Routers ---
# app.include_router(api_v1.router, prefix="/api/v1")
# app.include_router(auth_router, prefix="/api/v1")
# app.include_router(admin_router, prefix="/api/v1")
# app.include_router(github_router, prefix="/api/v1")
# app.include_router(llm_router, prefix="/api/v1")
# app.include_router(eval_router, prefix="/api/v1")
# # app.include_router(fb_router, prefix="/api/v1")
# app.include_router(analytics_router, prefix="/api/v1")

# # --- Root Endpoint ---
# @app.get("/")
# def root():
#     return {"message": "Welcome to PromptCraft backend!"}

# # --- Custom Exception Handlers ---

# # Global exception handler
# @app.exception_handler(Exception)
# async def global_exception_handler(request: Request, exc: Exception):
#     return JSONResponse(
#         status_code=500,
#         content={"error": "Internal server error", "details": str(exc)}
#     )

# # HTTP Exception handler (e.g., for 404, 401 errors)
# @app.exception_handler(HTTPException)
# async def http_exc_handler(req, exc):
#     return JSONResponse(
#         {"error_code": exc.status_code, "message": exc.detail},
#         status_code=exc.status_code
#     )

# # Validation error handler for pydantic models
# @app.exception_handler(ValidationError)
# async def validation_exc_handler(req, exc):
#     return JSONResponse(
#         {"error_code": 422, "message": "Validation Error", "details": exc.errors()},
#         status_code=422
#     )

# # Run the app with uvicorn when executed directly
# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
# # app.include_router(feedback_router, prefix='/feedback')
# # app.include_router(analytics_router, prefix='/analytics_router')
# from fastapi import Request
# from starlette.middleware.base import BaseHTTPMiddleware

# class FakeUserMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         request.state.user_id = "000000000000000000000001"  # dummy ObjectId
#         request.state.is_admin = True
#         return await call_next(request)

# app.add_middleware(FakeUserMiddleware)

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from pydantic import ValidationError

from app.routers import api_v1
from app.core.limiter import init_rate_limiter, rate_limit_exception_handler
from app.db.mongo import connect_to_mongo, close_db, get_db
from app.middleware.auth_middleware import AuthMiddleware  # Import the JWT auth middleware

# Routers
from app.api.v1.admin.routes import router as admin_router
from app.api.v1.auth.routes import router as auth_router
from app.api.v1.github.github_auth import router as github_router
from app.api.v1.llm.router import router as llm_router
from app.api.v1.evaluation.router import router as eval_router
# from app.api.v1.feedback.router import router as fb_router
from app.api.v1.feedback.router import router as feedback_router
from app.api.v1.analytics.router import router as analytics_router

# Initialize the FastAPI app
app = FastAPI(title="PromptCraft API", version="1.0")

# Add JWT auth middleware
app.add_middleware(AuthMiddleware)

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # In prod, use specific origins like ['https://example.com']
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Middleware to Inject DB/User ---
@app.middleware("http")
async def inject_db_and_user(request: Request, call_next):
    request.state.db = get_db()  # Get DB from the global state
    # Replace with actual logic to extract user info from token
    request.state.user_id = "64b123456789abcdef01234"  # Example user ID (for testing)
    request.state.is_admin = True  # Example admin status (for testing)
    response = await call_next(request)
    return response

# --- Rate Limiting Initialization ---
@app.on_event("startup")
async def startup_event():
    await init_rate_limiter(app)  # Initialize rate limiting
    await connect_to_mongo()  # Connect to MongoDB

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()  # Close MongoDB connection on shutdown

# Exception handler for rate limit (429)
app.add_exception_handler(429, rate_limit_exception_handler)

# --- Include Routers ---
app.include_router(api_v1.router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(github_router, prefix="/api/v1")
app.include_router(llm_router, prefix="/api/v1")
app.include_router(eval_router, prefix="/api/v1")
# app.include_router(fb_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")

# --- Root Endpoint ---
@app.get("/")
def root():
    return {"message": "Welcome to PromptCraft backend!"}

# --- Custom Exception Handlers ---

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "details": str(exc)}
    )

# HTTP Exception handler (e.g., for 404, 401 errors)
@app.exception_handler(HTTPException)
async def http_exc_handler(req, exc):
    return JSONResponse(
        {"error_code": exc.status_code, "message": exc.detail},
        status_code=exc.status_code
    )

# Validation error handler for pydantic models
@app.exception_handler(ValidationError)
async def validation_exc_handler(req, exc):
    return JSONResponse(
        {"error_code": 422, "message": "Validation Error", "details": exc.errors()},
        status_code=422
    )

# Run the app with uvicorn when executed directly
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
