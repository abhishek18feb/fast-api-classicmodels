from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_, between, not_
from fastapi import Depends, HTTPException, Path, APIRouter
from passlib.context import CryptContext
from models import Employees, Customers
from database import  SessionLocal
from starlette import status
from pydantic import  BaseModel, Field
from .empauth import get_current_emp

router = APIRouter(
    prefix='/employees',
    tags=['Employees']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
emp_dependency = Annotated[dict, Depends(get_current_emp)]

class EmpUserNamePassword(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=1, max_length=100)

@router.get('/', status_code=status.HTTP_200_OK)
async def select_emp_last_names(db: db_dependency, emp:emp_dependency):
    emp_records = db.query(Employees.lastName).all()
    if emp_records is None:
        raise HTTPException(status_code=400, detail="No records found")
    return [emp[0] for emp in emp_records]

@router.get("/select-multiple-fields", status_code=status.HTTP_200_OK)
async def select_emp_multiple_fields(db:db_dependency, emp:emp_dependency):
    emp_records = db.query(Employees.firstName, Employees.lastName, Employees.jobTitle).all()
    if emp_records is None:
        raise HTTPException(status_code=400, detail="No records found")
    return list(map(lambda emp:{"firstName":emp[0], "lastName":emp[1], "jobTitle":emp[2]}, emp_records))

@router.get("/select-all-fields", status_code=status.HTTP_200_OK)
async def select_emp_all_fields(db:db_dependency, emp:emp_dependency):
    emp_records = db.query(Employees).all()
    return emp_records

@router.get("/concat-query-example", status_code=status.HTTP_200_OK)
async def select_concat_example(db:db_dependency, emp:emp_dependency):
    emp_records = db.query(func.concat(Employees.firstName, " ", Employees.lastName)).all()
    
    return [emp[0] for emp in emp_records]


@router.patch("/create-password/{emp_id}", status_code=status.HTTP_200_OK)
async def update_create_emp_password(db: db_dependency,  emp_body:EmpUserNamePassword, emp_id:int=Path(gt=0)):
    emp_model = db.query(Employees).get(emp_id)
    if emp_model is None:
        raise HTTPException(status_code=404, detail="Emp not found")
    emp_model.username = emp_body.username
    emp_model.hashed_password = bcrypt_context.hash(emp_body.password)
    db.add(emp_model)
    db.commit()
    return emp_model

@router.get("/get-associated-customer", status_code=status.HTTP_200_OK)
async def get_associated_customer(db:db_dependency, emp:emp_dependency):
    if emp is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    print(emp)
    result = db.execute(
        select(Employees, Customers)
        .join(Customers, Employees.employeeNumber == Customers.salesRepEmployeeNumber)
        .where(Employees.employeeNumber == emp.get('id'))
    ).all()
    return [{"employee": emp.__dict__, "customer": cust.__dict__} for emp, cust in result]

@router.get("/order-by-null-values", status_code=status.HTTP_200_OK)
def order_by_null_values(db:db_dependency):
    results = db.query(Employees.firstName, Employees.lastName, Employees.reportsTo).order_by(Employees.reportsTo.desc()).all()

    return [{"firstName":firstName, "lastName":lastName, "reportsTo":reportsTo}
            for firstName, lastName, reportsTo in results
            ]

"""
 Where Clause Query
"""
@router.get("/where-job-title/{jobtitle}")
def select_emp_by_job_title(db:db_dependency, jobtitle:str = Path(..., min_length=3), officeCode=1):
    results = db.query(Employees.firstName, Employees.lastName, Employees.jobTitle, Employees.officeCode).filter(Employees.jobTitle == jobtitle).filter(Employees.officeCode==officeCode).all()
    return [{"firstName":firstName, "lastName":lastName, "jobTitle":jobTitle, "officeCode":officeCode} for firstName, lastName, jobTitle, officeCode in results]

@router.get("/where-with-or-condition/{jobtitle}/{officeCode}")
def select_where_with_or_clause(db:db_dependency, jobtitle:str=Path(min_length=1), officeCode:int = Path(gt=0)):
    results = db.query(Employees.firstName, Employees.lastName, Employees.jobTitle, Employees.officeCode).filter(or_(
        Employees.jobTitle == jobtitle,
        Employees.officeCode == officeCode
    )).order_by(
        Employees.officeCode,
        Employees.jobTitle
    ).all()

    data = [{"firstName":firstName, "lastName":lastName, "jobTitle":jobTitle, "officeCode":officeCode} for firstName, lastName, jobTitle, officeCode in results]

    return {"data":data, "totalRecords":len(data)}

@router.get("/where-with-between-nd-and")
def select_where_with_between_nd_and(db:db_dependency):
    results = db.query(Employees.firstName, Employees.lastName, Employees.jobTitle, Employees.officeCode).filter(between(Employees.officeCode, 1,3)).order_by(
        Employees.officeCode,
        Employees.jobTitle
    ).all()

    data = [{"firstName":firstName, "lastName":lastName, "jobTitle":jobTitle, "officeCode":officeCode} for firstName, lastName, jobTitle, officeCode in results]

    return {"data":data, "totalRecords":len(data)}

@router.get("/where-clause-with-like-operation")
def where_clause_with_like_operation(db:db_dependency):
    results = db.query(Employees.firstName, Employees.lastName, Employees.jobTitle, Employees.officeCode).filter(Employees.lastName.like('%son')).order_by(
        Employees.officeCode,
        Employees.jobTitle
    ).all()

    data = [{"firstName":firstName, "lastName":lastName, "jobTitle":jobTitle, "officeCode":officeCode} for firstName, lastName, jobTitle, officeCode in results]

    return {"data":data, "totalRecords":len(data)}

@router.get("/where-clause-with-in-clause")
def where_clause_with_in_clause(db:db_dependency):
    results = db.query(Employees.firstName, Employees.lastName, Employees.jobTitle, Employees.officeCode).filter(Employees.officeCode.in_([1,2,3])).order_by(Employees.officeCode).all()

    data = [{"firstName":firstName, "lastName":lastName, "jobTitle":jobTitle, "officeCode":officeCode} for firstName, lastName, jobTitle, officeCode in results]

    return {"data":data, "totalRecords":len(data)}

@router.get("/where-clause-with-is-null-operator")
def whre_clause_with_is_null_operator(db:db_dependency):
    results = db.query(Employees.firstName, Employees.lastName, Employees.jobTitle, Employees.officeCode).filter(Employees.reportsTo.is_(None)).order_by(Employees.officeCode).all()

    data = [{"firstName":firstName, "lastName":lastName, "jobTitle":jobTitle, "officeCode":officeCode} for firstName, lastName, jobTitle, officeCode in results]

    return {"data":data, "totalRecords":len(data)}

@router.get("/where-clause-with-not-equal-to")
def whre_clause_with_not_equal_to(db:db_dependency):
    results = db.query(Employees.firstName, Employees.lastName, Employees.jobTitle, Employees.officeCode).filter(Employees.jobTitle != 'Sales Rep').order_by(Employees.officeCode).all()

    data = [{"firstName":firstName, "lastName":lastName, "jobTitle":jobTitle, "officeCode":officeCode} for firstName, lastName, jobTitle, officeCode in results]

    return {"data":data, "totalRecords":len(data)}

@router.get("/where-clause-with-less-than-equal-to")
def whre_clause_with_less_than_equal_to(db:db_dependency):
    results = db.query(Employees.firstName, Employees.lastName, Employees.jobTitle, Employees.officeCode).filter(Employees.officeCode <= 4).order_by(Employees.officeCode).all()

    data = [{"firstName":firstName, "lastName":lastName, "jobTitle":jobTitle, "officeCode":officeCode} for firstName, lastName, jobTitle, officeCode in results]

    return {"data":data, "totalRecords":len(data)}

@router.get("/select-distinct-clause")
def select_distinct_clause(db:db_dependency):
    results = db.query(Employees.lastName).distinct().order_by(Employees.lastName).all()
    print("results", results)
    data = [{ "lastName":lastName[0]} for lastName in results]

    return {"data":data, "totalRecords":len(data)}

@router.get("/mysql-like-operater", status_code=status.HTTP_200_OK)
def mysql_like_clause(db:db_dependency):
    results = db.query(Employees.employeeNumber, Employees.lastName, Employees.firstName)\
                .filter(Employees.firstName.like('a%'))
    if results is not None:
        data = [{"employeeNumber":employeeNumber, "lastName":lastName, "firstName":firstName} for employeeNumber, lastName, firstName in results]
        return {"data":data, "total":len(data)}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Records not found") 
    
@router.get("/mysql-not-like-operator", status_code=status.HTTP_200_OK)
def mysql_not_like_operator(db:db_dependency):
    results = db.query(Employees.employeeNumber, Employees.lastName, Employees.firstName)\
                .filter((Employees.firstName.not_like('B%')))
    if results is not None:
        data = [{"employeeNumber":employeeNumber, "lastName":lastName, "firstName":firstName} for employeeNumber, lastName, firstName in results]
        return {"data":data, "total":len(data)}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Records not found") 
    
@router.get("/full-names", status_code=status.HTTP_200_OK)
def mysql_alias_get_fullname(db:db_dependency):
    results = db.query(func.concat_ws(", ", Employees.firstName, Employees.lastName).label("Full name")).order_by("Full name")
    # return results
    if results is not None:
        data = [{"full_name":name[0]} for name in results]
        return {"data":data, "total":len(data)}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Records not found") 
    







