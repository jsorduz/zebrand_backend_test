from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.routes.auth import router as auth_router
from app.routes.brands import router as brand_router
from app.routes.products import router as product_router
from app.routes.users import router as user_router

app = FastAPI(
    openapi_url="/openapi.json",
    docs_url="/docs",
)
app.include_router(auth_router, tags=["auth"])
app.include_router(user_router, tags=["users"])
app.include_router(product_router, tags=["products"])
app.include_router(brand_router, tags=["products"])


register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
