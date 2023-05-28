import time

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import OrderModel, DishModel, OrderDishModel
from ..schemas import OrderCreate, OrderStatus
from ..utils import verify_token, auth

router = APIRouter()


@router.post("/", status_code=201, response_model=OrderCreate)
def create_order(
    order: OrderCreate,
    token: HTTPAuthorizationCredentials = Depends(auth),
    db: Session = Depends(get_db),
):
    """
    Create a new order
    :param order: order data
    :param token: JWT token
    :param db: database session
    :return: created order
    :raise HTTPException: if dish not found or not enough dishes
    """
    verify_token(token.credentials)

    new_order = OrderModel(special_requests=order.special_requests, status="new")
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for dish in order.dishes:
        db_dish = db.query(DishModel).filter(DishModel.id == dish.dish_id).first()
        if db_dish is None:
            raise HTTPException(
                status_code=400, detail=f"Dish with id {dish.dish_id} not found"
            )
        if db_dish.quantity < dish.quantity:
            raise HTTPException(
                status_code=400, detail=f"Not enough dishes with id {dish.dish_id}"
            )

        order_dish = OrderDishModel(
            order_id=new_order.id,
            dish_id=dish.dish_id,
            quantity=dish.quantity,
            price=db_dish.price,
        )
        db.add(order_dish)

    db.commit()

    return OrderCreate(
        id=new_order.id,
        special_requests=new_order.special_requests,
        status=new_order.status,
        dishes=order.dishes,
    )


@router.get("/{id}", response_model=OrderStatus)
def read_order(
    id: int,
    token: HTTPAuthorizationCredentials = Depends(auth),
    db: Session = Depends(get_db),
):
    """
    Get order by id
    :param id: order id
    :param token: JWT token
    :param db: database session
    :return: order
    :raise HTTPException: if order not found
    """
    verify_token(token.credentials)
    order = db.query(OrderModel).filter(OrderModel.id == id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def process_order(order_id: int, db: Session):
    """
    Process order and mark it as completed in 10 seconds
    :param order_id: order id
    :param db: database session
    """
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if order is not None and order.status == "new":
        time.sleep(10)
        order.status = "completed"
        db.commit()
        db.refresh(order)


@router.post("/{id}/process")
async def process_order_endpoint(
    id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    background_tasks.add_task(process_order, id, db)
    return {"message": "Order is being processed"}
