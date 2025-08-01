from fastapi import APIRouter

router = APIRouter()

# Example route
@router.get("/hello")
async def hello():
    return {"message": "Hello from auth router"}
