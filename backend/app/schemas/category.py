from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    category_name: str
    subcategory: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    category_name: Optional[str] = None
    subcategory: Optional[str] = None

class CategoryResponse(CategoryBase):
    category_id: int

    model_config = {
        "from_attributes": True
    }