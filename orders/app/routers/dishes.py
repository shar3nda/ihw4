from typing import List

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import DishModel
from ..schemas import Dish, DishCreate
from ..utils import verify_token, auth

router = APIRouter()


@router.get("/", response_model=List[Dish])
def read_dishes(
    token: HTTPAuthorizationCredentials = Depends(auth),
    db: Session = Depends(get_db),
):
    """
    Get menu (list of all dishes)
    :param token: JWT token
    :param db: database session
    :return: list of all dishes
    """
    verify_token(token.credentials)
    # Get all dishes with quantity > 0 and order by name
    dishes = (
        db.query(DishModel)
        .filter(DishModel.quantity > 0)
        .order_by(DishModel.name)
        .all()
    )
    return dishes


@router.post("/", response_model=Dish)
def create_dish(
    dish: DishCreate,
    token: HTTPAuthorizationCredentials = Depends(auth),
    db: Session = Depends(get_db),
):
    """
    Create a new dish

    :param dish: dish data
    :param token: JWT token
    :param db: database session
    :return: created dish
    :raise HTTPException: if dish not found
    """
    verify_token(token.credentials)
    db_dish = DishModel(**dish.dict())
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


@router.get("/{id}", response_model=Dish)
def read_dish(
    id: int,
    token: HTTPAuthorizationCredentials = Depends(auth),
    db: Session = Depends(get_db),
):
    """
    Get dish by id
    :param id: dish id
    :param token: JWT token
    :param db: database session
    :return: requested dish
    :raise HTTPException: if dish not found
    """
    verify_token(token.credentials)
    db_dish = db.query(DishModel).filter(DishModel.id == id).first()
    if db_dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    return db_dish


@router.put("/{id}", response_model=Dish)
def update_dish(
    id: int,
    dish: DishCreate,
    token: HTTPAuthorizationCredentials = Depends(auth),
    db: Session = Depends(get_db),
):
    """
    Update dish by id
    :param id: dish id
    :param dish: dish data
    :param token: JWT token
    :param db: database session
    :return: updated dish
    :raise HTTPException: if dish not found
    """
    verify_token(token.credentials)
    db_dish = db.query(DishModel).filter(DishModel.id == id).first()
    if db_dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    for key, value in dish.dict().items():
        setattr(db_dish, key, value)
    db.commit()
    db.refresh(db_dish)
    return db_dish


@router.delete("/{id}", response_model=Dish)
def delete_dish(
    id: int,
    token: HTTPAuthorizationCredentials = Depends(auth),
    db: Session = Depends(get_db),
):
    """
    Delete dish by id
    :param id: dish id
    :param token: JWT token
    :param db: database session
    :return: deleted dish
    :raise HTTPException: if dish not found
    """
    verify_token(token.credentials)
    db_dish = db.query(DishModel).filter(DishModel.id == id).first()
    if db_dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    db.delete(db_dish)
    db.commit()
    return db_dish
