from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ReviewBase(BaseModel):
    product_id: int = Field(ge=1)
    customer_id: int = Field(ge=1)
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(default=None, max_length=1000)

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    review_id: int
    created_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }
