from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse
)
from app.services import category_service
from app.core.dependencies import get_db
from Admin.admin_auth import get_current_admin

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return category_service.create_category(db, payload)


@router.get(
    "/",
    response_model=List[CategoryResponse]
)
def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return category_service.get_all_categories(db, skip=skip, limit=limit)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse
)
def get_category(
    category_id: str,
    db: Session = Depends(get_db)
):
    return category_service.get_category_by_id(db, category_id)


@router.put(
    "/{category_id}",
    response_model=CategoryResponse
)
def update_category(
    category_id: str,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return category_service.update_category(db, category_id, payload)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_category(
    category_id: str,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    category_service.delete_category(db, category_id)
