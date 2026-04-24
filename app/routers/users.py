from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from app.database import get_db
from app.schemas.users import UsersCreate, UsersLogin, UsersOutput, UserRefresh
from app.utils.hashing import Hasher
from app.utils.jwt import verify_token, create_refresh_token, create_access_token
from app.auth.dependencies import get_current_user
from app.models.users import Users
from app.models.sessions import Session
from app.config.settings import settings

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register", response_model=UsersOutput)
async def register_user(user: UsersCreate, db: AsyncSession = Depends(get_db)):
    result =  (await db.execute(select(Users).where(Users.email == user.email)))
    exist_user = result.scalar_one_or_none()
    exist_phone = (await db.execute(select(Users).where(Users.phone == user.phone))).scalars().first()
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    if exist_phone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone number already exists",
        )

    hashed_password = Hasher.get_password_hash(user.password)
    new_user = Users(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password=hashed_password,
        role=user.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login")
async def login(user: UsersLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Users).where(Users.email == user.email))
    db_user = result.scalar_one_or_none()
    if not db_user or not Hasher.verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User does not exist or Incorrect password",
        )
    access_token = create_access_token(data={"sub": str(db_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(db_user.id)})

    create_session = Session(
    user_id=db_user.id,
    token=refresh_token,  # store refresh token not access token
    expires_at=datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    db.add(create_session)
    await db.commit()
    await db.refresh(create_session)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "type":"Bearer"
    }

@router.post("/refresh")
async def refresh(user: UserRefresh, db: AsyncSession = Depends(get_db)):
    verified_token = verify_token(user.token)
    if not verified_token:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invalid token",
        )

    user_id : str = verified_token.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invalid token"
        )

    session_exist = (await db.execute(select(Session).where(Session.token == user.token))).scalar_one_or_none()
    if not session_exist or session_exist.is_revoked:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Session does not exist",
        )
    new_access_token = create_access_token(data={"sub": user_id})
    return new_access_token

@router.post("/logout")
async def logout(user: UserRefresh, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = (await db.execute(select(Session).where(Session.token == user.token)))
    token_exist = result.scalar_one_or_none()

    if not token_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Session does not exist",
        )
    token_exist.is_revoked = True
    await db.commit()
    return "Successfully logged out"

@router.get("/me")
async def me(current_user = Depends(get_current_user)):
    return current_user
