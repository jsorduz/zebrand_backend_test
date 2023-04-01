from fastapi import APIRouter, Depends, status

from app.models import Brand as BrandModel
from app.routes.deps import get_brand_from_db, get_current_user
from app.schemas import BrandCreateSchema, BrandSchema, BrandUpdateSchema

router = APIRouter()


@router.get(
    "/brands/",
    dependencies=[Depends(get_current_user)],
    response_model=list[BrandSchema],
)
async def list_brands(
    offset: int = 0,
    limit: int = 100,
    order_by: str = "name",
) -> list[BrandModel]:
    return await BrandModel.all().order_by(order_by).offset(offset).limit(limit)


@router.post(
    "/brands/",
    dependencies=[Depends(get_current_user)],
    response_model=BrandSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_brand(brand_in: BrandCreateSchema) -> BrandModel:
    return await BrandModel.create(**brand_in.dict(exclude_unset=True))


@router.get(
    "/brands/{brand_id}/",
    dependencies=[Depends(get_current_user)],
    response_model=BrandSchema,
)
async def retrieve_brand(
    brand: BrandModel = Depends(get_brand_from_db),
) -> BrandModel | None:
    return brand


@router.patch(
    "/brands/{brand_id}/",
    dependencies=[Depends(get_current_user)],
    response_model=BrandSchema,
)
async def patch_brand(
    brand_in: BrandUpdateSchema, brand: BrandModel = Depends(get_brand_from_db)
):
    update_data = brand_in.dict(exclude_unset=True)
    for field, _ in update_data.items():
        setattr(brand, field, update_data[field])
    await brand.save()
    return await BrandModel.get(id=brand.id)


@router.delete(
    "/brands/{brand_id}/",
    dependencies=[Depends(get_current_user)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_brand(brand: BrandModel = Depends(get_brand_from_db)):
    await brand.delete()
