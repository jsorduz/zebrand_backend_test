from uuid import UUID

from fastapi import HTTPException, status

from app.models import User as UserModel


async def get_user_from_db(user_id: UUID) -> UserModel:
    user = await UserModel.get(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )
    return user
