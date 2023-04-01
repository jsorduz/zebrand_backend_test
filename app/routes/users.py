from fastapi import APIRouter, Depends, status

from app.models import User as UserModel
from app.routes.deps import get_current_user, get_user_from_db
from app.schemas import UserCreateSchema, UserSchema, UserUpdateSchema

router = APIRouter()


@router.get(
    "/users/",
    dependencies=[Depends(get_current_user)],
    response_model=list[UserSchema],
)
async def list_users(
    offset: int = 0,
    limit: int = 100,
    order_by: str = "email",
) -> list[UserModel]:
    return await UserModel.all().order_by(order_by).offset(offset).limit(limit)


@router.post(
    "/users/",
    dependencies=[Depends(get_current_user)],
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user_in: UserCreateSchema) -> UserModel:
    return await UserModel.create(
        **user_in.dict(exclude_unset=True),
        hashed_password=UserModel.hash_password(user_in.password),
    )


@router.get(
    "/users/{user_id}/",
    dependencies=[Depends(get_current_user)],
    response_model=UserSchema,
)
async def retrieve_user(
    user: UserModel = Depends(get_user_from_db),
) -> UserModel | None:
    return user


@router.patch(
    "/users/{user_id}/",
    dependencies=[Depends(get_current_user)],
    response_model=UserSchema,
)
async def patch_user(
    user_in: UserUpdateSchema, user: UserModel = Depends(get_user_from_db)
):
    update_data = user_in.dict(exclude_unset=True)
    for field, _ in update_data.items():
        setattr(user, field, update_data[field])
    await user.save()
    return await UserModel.get(id=user.id)


@router.delete(
    "/users/{user_id}/",
    dependencies=[Depends(get_current_user)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(user: UserModel = Depends(get_user_from_db)):
    await user.delete()
