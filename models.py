from tortoise.models import Model
from tortoise import fields


class Product(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    description = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "products"

    def __str__(self):
        return self.name