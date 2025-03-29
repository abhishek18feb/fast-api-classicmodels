from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_, and_
from fastapi import Depends, HTTPException, Path, APIRouter
from database import  SessionLocal
from starlette import status
from pydantic import  BaseModel, Field
from models import Offices



router = APIRouter(
    prefix='/offices',
    tags=['Offices']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

@router.get('get-offices-using-in-clause')
def get_offices_using_in_clause(db:db_dependency):
    results = db.query(Offices.officeCode, Offices.city, Offices.phone, Offices.country).filter(Offices.country.in_(['USA' , 'France'])).all()
    if results is not None:
        data = [{"officeCode":officeCode, "city":city, "phone":phone, "country": country} for officeCode, city, phone, country in results]
        return {"data":data, "total":len(data)}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No record found")
    
@router.get('get-offices-using-not-in-clause')
def get_offices_using_not_in_clause(db:db_dependency):
    results = db.query(Offices.officeCode, Offices.city, Offices.phone, Offices.country).filter(Offices.country.not_in(['USA' , 'France'])).all()
    if results is not None:
        data = [{"officeCode":officeCode, "city":city, "phone":phone, "country": country} for officeCode, city, phone, country in results]
        return {"data":data, "total":len(data)}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No record found")
    
