from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select, func, case
from fastapi import Depends, HTTPException, Path, APIRouter
from database import  SessionLocal
from starlette import status
from pydantic import  BaseModel, Field
from models import Orders, OrderDetails

router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/get-order-detail-by-qyantiay-multiply-price")
def get_order_detail_by_quant_mul_price(db:db_dependency):
    # Construct the query
    query = (
    db.query(
        OrderDetails.orderNumber,
        OrderDetails.orderLineNumber,
        (OrderDetails.quantityOrdered * OrderDetails.priceEach).label('totalPrice')
    )
    .order_by((OrderDetails.quantityOrdered * OrderDetails.priceEach).desc())
    )

    # Execute the query and fetch results
    results = query.all()

    for result in results:
        print(result.orderNumber, result.orderLineNumber, result.totalPrice)
    
    return [{
        "orderNumber":orderNumber,
        "orderLineNumber":orderLineNumber,
        "totalPrice":totalPrice,
        } for orderNumber,orderLineNumber, totalPrice  in results]

@router.get("/order-by-using-custom-list", status_code=status.HTTP_200_OK)
def order_by_using_custom_list(db:db_dependency):
    sortedOrder = case({
        'In Process':1,
        'On Hold':2, 
        'Cancelled':3, 
        'Resolved':4, 
        'Disputed':5, 
        'Shipped':6
    }, value=Orders.status)

    results = db.query(Orders.customerNumber, Orders.status).order_by(sortedOrder).all()
    return [{"customerNumber":customerNumber, "status":status} for customerNumber, status in results]

@router.get("/get-orders-range-between-date", status_code=status.HTTP_200_OK)
def get_product_range_between_date(db:db_dependency):
    results = db.query(Orders.orderNumber, Orders.requiredDate, Orders.status)\
                .filter(Orders.requiredDate.between('2003-01-01', '2003-01-31')).all()
    if results is not None:
        data = [{"orderNumber":orderNumber, "requiredDate":requiredDate, "status":status} for orderNumber, requiredDate, status in results]
        return {"data":data, "total":len(data)}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No record found")

