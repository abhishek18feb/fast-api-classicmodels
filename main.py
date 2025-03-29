from fastapi import FastAPI
import models
from database import engine
from routers import  employees, empauth, customer, orders, offices, products

app = FastAPI()

@app.get("/")
def health_check():
    return {'status':True}

models.Base.metadata.create_all(bind=engine)

app.include_router(employees.router)
app.include_router(empauth.router)
app.include_router(customer.router)
app.include_router(orders.router)
app.include_router(offices.router)
app.include_router(products.router)

