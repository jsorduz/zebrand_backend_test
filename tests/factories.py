from app.models import User


async def create_user(email: str, password: str):
    # TODO: create a factory method that creates more than one user at the same time with dummy values
    return await User.create(email=email, hashed_password=User.hash_password(password))
