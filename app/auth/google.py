from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.config.settings import settings
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse
from app.database import get_db
import httpx
from app.models.users import Users, AuthProvider, Role
from app.utils.jwt import create_access_token, create_refresh_token
from app.utils.hashing import Hasher
from pydantic import BaseModel
from app.middleware.rate_limit import limiter


router = APIRouter(
    prefix="/google",
    tags=["Google"]
)

@router.get("/")
async def google_login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid email profile"
    )
    return RedirectResponse(google_auth_url)

@limiter.limit("10/minute")
@router.get("/callback")
async def google_callback(request: Request, code: str, db: AsyncSession = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }
        )
        token_data =  token_response.json()
        access_token = token_data.get("access_token")

        user_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_info = await user_response.json()

    email = user_info.get("email")
    name = user_info.get("name")
    avatar = user_info.get("picture")

    result = await db.execute(select(Users).where(Users.email == email))
    already_exist = result.scalar_one_or_none()

    if not already_exist:
        new_user = Users(
            name=name,
            email=email,
            avatar=avatar,
            provider=AuthProvider.google,
            password=None
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        already_exist = new_user

    if already_exist and not already_exist.is_profile_complete:
        return RedirectResponse(f"http://localhost:5173/complete-profile?email={email}")

    jwt_token = create_access_token(data={"sub": already_exist.email})
    return RedirectResponse(f"http://localhost:5173/oauth?token={jwt_token}")

class CompleteProfile(BaseModel):
    email: str
    phone: str
    password: str
    role: Role

@limiter.limit("10/minute")
@router.post("/complete-profile")
async def complete_profile(request: Request,data: CompleteProfile, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Users).where(Users.email == data.email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.is_profile_complete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already complete"
        )

    user.phone = data.phone
    user.password = Hasher.get_password_hash(data.password)
    user.role = data.role
    user.is_profile_complete = True

    await db.commit()
    await db.refresh(user)

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }



