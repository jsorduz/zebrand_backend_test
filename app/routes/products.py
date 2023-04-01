from fastapi import APIRouter

router = APIRouter()


@router.get("/products/")
async def list_products():
    return {"message": "list products"}
