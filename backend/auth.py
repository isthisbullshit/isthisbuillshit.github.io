import uuid

from fastapi import APIRouter, Request
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


@router.get("/api/auth/status")
async def status(request: Request):
    auth_cookie = request.cookies.get("auth")
    return {"logged_in": auth_cookie is not None}


@router.post("/api/auth/logout")
async def logout():
    response = JSONResponse(
        content={
            "success": True,
            "message": "Logged out",
        }
    )
    response.delete_cookie(key="auth")
    return response
