from pydantic import BaseModel, Field
from typing import Optional

class CategoryBase(BaseModel):
    category_name: str = Field(min_length=1, max_length=255)
    subcategory: Optional[str] = Field(default=None, max_length=255)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    category_name: Optional[str] = None
    subcategory: Optional[str] = None

class CategoryResponse(CategoryBase):
    category_id: str

    model_config = {
        "from_attributes": True
    }
