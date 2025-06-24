from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_, between, not_
from fastapi import Depends, HTTPException, Path, APIRouter
from passlib.context import CryptContext
from models import Member, Committee
from database import  SessionLocal
from starlette import status
from pydantic import  BaseModel, Field
from .empauth import get_current_emp
from typing import List

router = APIRouter(
    prefix='/memjoin',
    tags=['Memjoin']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class MemberCreate(BaseModel):
    name: str

class CommitteeCreate(BaseModel):
    name: str

@router.post("/insert-members-data")
def insert_members_data(members: List[MemberCreate], db: Session = Depends(get_db)):
    db_members = [Member(name=member.name) for member in members]
    db.add_all(db_members)
    db.commit()
    return {"message": "Members inserted successfully"}

@router.post("/insert-committee-data")
def insert_committee_data(committees: List[CommitteeCreate], db: Session = Depends(get_db)):
    db_committee = [Committee(name=committee.name) for committee in committees]
    db.add_all(db_committee)
    db.commit()
    return{"message": "Committe insterted successfully"}



