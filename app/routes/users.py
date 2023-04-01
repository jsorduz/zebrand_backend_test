from fastapi import APIRouter, status

router = APIRouter()


@router.get("/users/")
async def list_users():
    return {"message": "list users"}


@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user():
    return {"message": "create user"}


@router.get("/users/{user_id}/")
async def retrieve_user(user_id: int):
    return {"message": f"retrieve user {user_id}"}


@router.patch("/users/{user_id}/")
async def patch_user(user_id: int):
    return {"message": f"patch user {user_id}"}


@router.delete("/users/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    pass
