from pydantic import BaseModel, ConfigDict, EmailStr

from app.api.schemas.enterprise import EnterpriseShort


class UserFromDB(BaseModel):
    username: str
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    disabled: bool = False
    role: str | None = None

    class Config:
        from_attributes = True


class UserCreate(UserFromDB):
    model_config = ConfigDict(from_attributes=True)

    password: str


class UserLogin(UserFromDB):
    model_config = ConfigDict(from_attributes=True)

    password: str


class UserExtended(UserFromDB):
    model_config = ConfigDict(from_attributes=True)

    enterprises: list[EnterpriseShort]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
