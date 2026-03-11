from pydantic import BaseModel, Field

class WishlistBase(BaseModel):
    customer_id: int = Field(ge=1)
    product_id: int = Field(ge=1)

class WishlistCreate(WishlistBase):
    pass

class WishlistResponse(WishlistBase):
    wishlist_id: int

    model_config = {
        "from_attributes": True
    }
