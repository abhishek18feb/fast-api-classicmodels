from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_, and_, not_
from fastapi import Depends, HTTPException, Path, APIRouter
from database import  SessionLocal
from starlette import status
from pydantic import  BaseModel, Field
from models import Products



router = APIRouter(
    prefix='/products',
    tags=['Products']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/get-product-range-between-90-and-100")
def get_product_range_between_90_and_100(db:db_dependency):
    results = db.query(Products.productCode, Products.productName, Products.buyPrice)\
                .filter(Products.buyPrice.between(90, 100))
    if results is not None:
        data = [{"productCode":productCode, "productName":productName, "buyPrice":buyPrice} for productCode, productName, buyPrice in results]
        return {"data":data, "total":len(data)}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No record found")
    
@router.get("/get-product-range-not-between-20-and-100")
def get_product_range_not_between_90_and_100(db:db_dependency):
    results = db.query(Products.productCode, Products.productName, Products.buyPrice)\
                .filter(not_(Products.buyPrice.between(20, 100)))
    if results is not None:
        data = [{"productCode":productCode, "productName":productName, "buyPrice":buyPrice} for productCode, productName, buyPrice in results]
        return {"data":data, "total":len(data)}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No record found")
    
@router.get("/mysql-like-operator-with-escape", status_code=status.HTTP_200_OK)
def mysql_like_with_escape(db:db_dependency):
    results = db.query(Products.productCode, Products.productName)\
                .filter((Products.productCode.like('%\_20%')))
    if results is not None:
        data = [{"productCode":productCode, "productName":productName} for productCode, productName in results]
        return {"data":data, "total":len(data)}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Records not found")
    