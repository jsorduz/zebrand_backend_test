from fastapi import APIRouter, Depends, status

from app.models import Product as ProductModel
from app.routes.deps import get_current_user, get_product_from_db
from app.schemas import ProductCreateSchema, ProductSchema, ProductUpdateSchema

router = APIRouter()


@router.get(
    "/products/",
    dependencies=[Depends(get_current_user)],
    response_model=list[ProductSchema],
)
async def list_products(
    offset: int = 0,
    limit: int = 100,
    order_by: str = "name",
) -> list[ProductModel]:
    return await ProductModel.all().order_by(order_by).offset(offset).limit(limit)


@router.post(
    "/products/",
    dependencies=[Depends(get_current_user)],
    response_model=ProductSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(product_in: ProductCreateSchema) -> ProductModel:
    return await ProductModel.create(**product_in.dict(exclude_unset=True))


@router.get(
    "/products/{product_id}/",
    dependencies=[Depends(get_current_user)],
    response_model=ProductSchema,
)
async def retrieve_product(
    product: ProductModel = Depends(get_product_from_db),
) -> ProductModel | None:
    return product


@router.patch(
    "/products/{product_id}/",
    dependencies=[Depends(get_current_user)],
    response_model=ProductSchema,
)
async def patch_product(
    product_in: ProductUpdateSchema,
    product: ProductModel = Depends(get_product_from_db),
):
    update_data = product_in.dict(exclude_unset=True)
    for field, _ in update_data.items():
        setattr(product, field, update_data[field])
    await product.save()
    return await ProductModel.get(id=product.id)


@router.delete(
    "/products/{product_id}/",
    dependencies=[Depends(get_current_user)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(product: ProductModel = Depends(get_product_from_db)):
    await product.delete()
