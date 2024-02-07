from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.exc import NoResultFound

from app.api.schemas.user import Token, TokenData, UserCreate, UserExtended, UserFromDB
from app.services.user_service import UserService
from app.utils.auth import (
    create_access_token,
    get_token_payload,
    oauth2_scheme,
    verify_password,
)
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

user_router = APIRouter(prefix="", tags=["User"])


async def get_user_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> UserService:
    return UserService(uow)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], user_service: UserService = Depends(get_user_service)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = get_token_payload(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    try:
        user = await user_service.get_user_by_username(token_data.username)
    except NoResultFound:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[UserExtended, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@user_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], user_service: UserService = Depends(get_user_service)
) -> Token:
    try:
        user = await user_service.get_user_by_username_for_login(form_data.username)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@user_router.get("/users/current_user")
async def get_current_auth_user(
    current_user: Annotated[UserFromDB, Depends(get_current_active_user)],
):
    return current_user


@user_router.post("/users/user", status_code=status.HTTP_201_CREATED, response_model=UserFromDB)
async def create_user(user_data: UserCreate, user_service: UserService = Depends(get_user_service)):
    try:
        user = await user_service.add_user(user_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}: Failed to create user")
    return user
