from fastapi import APIRouter, BackgroundTasks, Depends, Request, status
from fastapi.logger import logger

from app.models import Product as ProductModel
from app.routes.deps import (
    get_current_user,
    get_current_user_or_none,
    get_product_from_db,
)
from app.schemas import ProductCreateSchema, ProductSchema, ProductUpdateSchema

router = APIRouter()


async def increase_product_views(request: Request, product: ProductModel):
    """
    TODO: Do something with the request data for further understanding of who and how is the products been queried
    """
    product.views += 1
    await product.save()


async def notify_product_change(
    product_before: dict | None, product_after: dict | None
):
    """
    TODO: Implement a third party email provider to send emails when a change is detected
            We have the data and the cases, it is just use them
    """
    if product_before is None and product_after is None:
        raise "Unexpected behavior, it is expected a product creation, update or delete"
    if product_before is None:
        logger.info(f"Added new product: {product_after}")
        return
    if product_after is None:
        logger.info(f"Deleted product: {product_before}")
        return
    for key, value in product_before.items():
        if key != "updated_at" and product_after[key] != value:
            logger.info(f"Updated product: {product_after}")
            return


@router.get(
    "/products/",
    # Admin and Anonymous users can query this endpoints without restrictions
    # dependencies=[Depends(get_current_user)],
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
async def create_product(
    background_tasks: BackgroundTasks, product_in: ProductCreateSchema
) -> ProductModel:
    product = await ProductModel.create(**product_in.dict(exclude_unset=True))
    background_tasks.add_task(
        notify_product_change, None, ProductSchema.from_orm(product).dict()
    )
    return product


@router.get("/products/{product_id}/", response_model=ProductSchema)
async def retrieve_product(
    request: Request,
    background_tasks: BackgroundTasks,
    product: ProductModel = Depends(get_product_from_db),
    current_user=Depends(get_current_user_or_none),
) -> ProductModel | None:
    # Anonymous user is querying an specific product, we need to increase its views
    if current_user is None:
        background_tasks.add_task(increase_product_views, request, product)
    return product


@router.patch(
    "/products/{product_id}/",
    dependencies=[Depends(get_current_user)],
    response_model=ProductSchema,
)
async def patch_product(
    background_tasks: BackgroundTasks,
    product_in: ProductUpdateSchema,
    product: ProductModel = Depends(get_product_from_db),
):
    # Store product data before patch
    product_before_dict = ProductSchema.from_orm(product).dict()
    update_data = product_in.dict(exclude_unset=True)
    for field, _ in update_data.items():
        setattr(product, field, update_data[field])
    await product.save()
    product = await ProductModel.get(id=product.id)
    background_tasks.add_task(
        notify_product_change,
        product_before_dict,
        ProductSchema.from_orm(product).dict(),
    )
    return product


@router.delete(
    "/products/{product_id}/",
    dependencies=[Depends(get_current_user)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(
    background_tasks: BackgroundTasks,
    product: ProductModel = Depends(get_product_from_db),
):
    background_tasks.add_task(
        notify_product_change, ProductSchema.from_orm(product).dict(), None
    )
    await product.delete()
