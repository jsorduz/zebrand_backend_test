from fastapi import FastAPI

app = FastAPI()


@app.get("/products/")
async def list_products():
    return {"message": "list products"}


@app.get("/users/")
async def list_users():
    return {"message": "list users"}
