# from fastapi import Request
# from starlette.middleware.base import BaseHTTPMiddleware
# from fastapi.exceptions import HTTPException
# from starlette.status import HTTP_401_UNAUTHORIZED

# PUBLIC_PATHS = [
#     "/",  # Allow root path
#     "/favicon.ico",  # Allow favicon
#     "/api/v1/auth/signup",
#     "/api/v1/auth/login",
#     "/docs",
#     "/openapi.json"
# ]

# class AuthMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         path = request.url.path
#         if path in PUBLIC_PATHS or path.startswith("/static"):
#             return await call_next(request)

#         auth_header = request.headers.get("Authorization")
#         if not auth_header or not auth_header.startswith("Bearer "):
#             raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Authorization token missing")

#         # Optional: Extract and verify token here, attach to request.state.user if needed

#         return await call_next(request)

# from fastapi import Request
# from starlette.middleware.base import BaseHTTPMiddleware
# from fastapi.exceptions import HTTPException
# from starlette.status import HTTP_401_UNAUTHORIZED

# PUBLIC_PATHS = [
#     "/",  # Allow root path
#     "/favicon.ico",  # Allow favicon
#     "/api/v1/auth/signup",
#     "/api/v1/auth/login",
#     "/docs",
#     "/openapi.json"
# ]

# class AuthMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         path = request.url.path
#         if path in PUBLIC_PATHS or path.startswith("/static"):
#             return await call_next(request)

#         auth_header = request.headers.get("Authorization")

#         # TEMP bypass for Swagger or local dev
#         if not auth_header or not auth_header.startswith("Bearer "):
#             request.state.user_id = "test_user_id"
#             return await call_next(request)

#         # TODO: Validate token here and set request.state.user_id
#         return await call_next(request)


from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

# Publicly accessible paths (no authentication required)
PUBLIC_PATHS = [
    "/",  # Root
    "/favicon.ico",
    "/api/v1/auth/signup",
    "/api/v1/auth/login",
    "/docs",
    "/openapi.json"
]

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # ✅ Allow all OPTIONS requests for CORS preflight
        if request.method == "OPTIONS":
            return await call_next(request)

        # ✅ Allow public paths and static files
        if path in PUBLIC_PATHS or path.startswith("/static"):
            return await call_next(request)

        # ✅ TEMP bypass auth for development
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            request.state.user_id = "test_user_id"  # Set a default dev user
            return await call_next(request)

        # 🔐 TODO: Implement token validation logic here
        # token = auth_header.split(" ")[1]
        # user_id = validate_token_and_get_user_id(token)
        # request.state.user_id = user_id

        return await call_next(request)


