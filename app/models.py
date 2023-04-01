from tortoise import fields
from tortoise.models import Model

VARCHAR_MAX_LENGTH = 255


class UUIDMixin(Model):
    id = fields.UUIDField(pk=True)

    class Meta:
        abstract = True


class TimeStampedMixin(Model):
    created_at = fields.DatetimeField(null=False, auto_now_add=True)
    updated_at = fields.DatetimeField(null=False, auto_now=True)

    class Meta:
        abstract = True


class User(UUIDMixin, TimeStampedMixin):
    email = fields.CharField(
        max_length=VARCHAR_MAX_LENGTH, null=False, unique=True, index=True
    )
    hashed_password = fields.CharField(max_length=VARCHAR_MAX_LENGTH, null=False)

    class Meta:
        table: str = "users"

    @classmethod
    def hash_password(cls, password: str):
        # TODO: implement a hash password algorithm
        return f"hashed-{password}"


class Brand(UUIDMixin, TimeStampedMixin):
    name = fields.CharField(
        max_length=VARCHAR_MAX_LENGTH, null=False, unique=True, index=True
    )

    class Meta:
        table: str = "brands"


class Product(UUIDMixin, TimeStampedMixin):
    sku = fields.CharField(
        max_length=VARCHAR_MAX_LENGTH, null=False, unique=True, index=True
    )
    name = fields.CharField(max_length=VARCHAR_MAX_LENGTH, null=False)
    price = fields.FloatField(null=False)
    views = fields.IntField(default=0)
    brand = fields.ForeignKeyField(
        "models.Brand", related_name="products", on_delete=fields.RESTRICT, null=True
    )

    class Meta:
        table: str = "products"
