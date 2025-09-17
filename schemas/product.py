from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    name: str = Field(..., min_length=2, max_length=12)
    price: float = Field(..., gt=1)
    in_stock: bool | None = None

    # Optional Field
    discount: Optional[float] = None