from pydantic import BaseModel

class WishlistBase(BaseModel):
    customer_id: int
    product_id: int

class WishlistCreate(WishlistBase):
    pass

class WishlistResponse(WishlistBase):
    wishlist_id: int

    model_config = {
        "from_attributes": True
    }