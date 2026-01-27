import uuid

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/api/auth/login")
async def login():
    auth_token = str(uuid.uuid4())
    response = JSONResponse(
        content={
            "success": True,
            "message": "Logged in",
            "token": auth_token,
        }
    )
    response.set_cookie(key="auth", value=auth_token)
    return response
