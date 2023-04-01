from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UUIDPkMixin(BaseModel):
    id: UUID

    class Config:
        orm_mode = True


class TimeStampedMixin(BaseModel):
    created_at: datetime
    updated_at: datetime


class UserBaseSchema(BaseModel):
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    password: str


class UserUpdateSchema(UserBaseSchema):
    """
    Only allow to change email, the password update should be done only by the same user
    """

    pass


class UserSchema(UUIDPkMixin, TimeStampedMixin, UserBaseSchema):
    pass


class BrandBaseSchema(BaseModel):
    name: str


class BrandCreateSchema(BrandBaseSchema):
    pass


class BrandUpdateSchema(BrandBaseSchema):
    pass


class BrandSchema(UUIDPkMixin, TimeStampedMixin, BrandBaseSchema):
    pass
