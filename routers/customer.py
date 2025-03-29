from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_, and_
from fastapi import Depends, HTTPException, Path, APIRouter
from database import  SessionLocal
from starlette import status
from pydantic import  BaseModel, Field
from models import Customers



router = APIRouter(
    prefix='/customers',
    tags=['Customers']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/get-customer-fn-ln-orderby", status_code=status.HTTP_200_OK)
def get_customer_fn_ln_order_by(db:db_dependency):
    results = db.query(Customers.contactFirstName, Customers.contactLastName).order_by(Customers.contactLastName.desc(), Customers.contactFirstName.asc()).all()
    if results is not None:
        return [{"firstName":contactFirstName, "lastName":contactLastName} for contactFirstName, contactLastName in results]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No record found")
    
@router.get("/select-distinct-with-multiple-clause")
def select_distinct_with_multiple_clause(db:db_dependency):
    results = db.query(Customers.state, Customers.city).distinct().filter(Customers.state.is_not(None)).order_by(Customers.state, Customers.city.desc()).all()
    if results is not None:
        data = [{"state":state, "city":city} for state, city in results]
        return {"data":data, "total":len(data)}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No record found")
    
@router.get("/where-with-multiple-and-condition")
def where_with_multiple_and_condition(db:db_dependency):
    results = db.query(Customers.customerName, Customers.country, Customers.state, Customers.creditLimit).filter(and_(
        Customers.country == 'USA', Customers.state == 'CA', Customers.creditLimit > 100000
    ))

    if results is not None:
        data = [{"customerName":customerName, "state":state, "city":city, "creditlimit":creditLimit} for customerName, state, city, creditLimit in results]
        return {"data":data, "total":len(data)}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No record found")
    
@router.get("/where-with-multiple-or-nd-and-condition")
def where_with_multiple_or_nd_and_condition(db:db_dependency):
    results = db.query(Customers.customerName, Customers.country, Customers.state, Customers.creditLimit).filter(
        or_(
        Customers.country == 'USA', Customers.country == 'France',
    )).filter(Customers.state.is_not(None)).filter(Customers.creditLimit > 100000).all()

    if results is not None:
        data = [{"customerName":customerName, "country":country, "state":state, "creditlimit":creditLimit} for customerName,country, state, creditLimit in results]
        return {"data":data, "total":len(data)}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No record found")


    

