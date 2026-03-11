from pydantic import BaseModel, Field

class WishlistBase(BaseModel):
    customer_id: str = Field(min_length=1, max_length=50)
    product_id: str = Field(min_length=1, max_length=50)

class WishlistCreate(WishlistBase):
    pass

class WishlistResponse(WishlistBase):
    wishlist_id: str

    model_config = {
        "from_attributes": True
    }
