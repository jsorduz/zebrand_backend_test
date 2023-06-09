from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.models import Brand as BrandModel
from app.models import Product as ProductModel
from app.models import User as UserModel
from app.routes.auth import (
    ALGORITHM,
    SECRET_KEY,
    TokenData,
    oauth2_scheme,
    optional_oauth2_scheme,
)


async def get_user_from_db(user_id: UUID) -> UserModel:
    user = await UserModel.get(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )
    return user


async def get_brand_from_db(brand_id: UUID) -> BrandModel:
    brand = await BrandModel.get(id=brand_id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="brand not found",
        )
    return brand


async def get_product_from_db(product_id: UUID) -> ProductModel:
    product = await ProductModel.get(id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="product not found",
        )
    return product


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await UserModel.get(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_or_none(
    token: Annotated[str, Depends(optional_oauth2_scheme)]
):
    """
    We need to see who is querying an endpoint:
    - admin: request has auth header
    - anonymous user: no auth header
    """
    if not token:
        return

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await UserModel.get(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
