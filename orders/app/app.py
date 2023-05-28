from fastapi import FastAPI, Depends


from .database import engine
from .models import Base
from .routers import dishes, orders
from .utils import auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    dishes.router,
    prefix="/dishes",
    tags=["dishes"],
    dependencies=[Depends(auth)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    orders.router,
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(auth)],
    responses={404: {"description": "Not found"}},
)
