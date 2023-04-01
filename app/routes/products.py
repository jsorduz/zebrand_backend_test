from fastapi import APIRouter, status

router = APIRouter()


@router.get("/products/")
async def list_products():
    return {"message": "list products"}


@router.post("/products/", status_code=status.HTTP_201_CREATED)
async def create_product():
    return {"message": "create product"}


@router.get("/products/{product_id}/")
async def retrieve_product(product_id: int):
    return {"message": f"retrieve product {product_id}"}


@router.patch("/products/{product_id}/")
async def patch_product(product_id: int):
    return {"message": f"patch product {product_id}"}


@router.delete("/products/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int):
    pass
