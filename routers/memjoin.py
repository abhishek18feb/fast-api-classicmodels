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

@router.get('insert-members-data')
def insert_members_data(db:db_dependency):
    members = [
        Member(name="John"),
        Member(name="Jane"),
        Member(name="Mary"),
        Member(name="David"),
        Member(name="Amelia")
    ]
    db.add_all(members)
    db.commit()





