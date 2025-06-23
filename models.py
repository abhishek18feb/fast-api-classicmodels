from database import Base
from sqlalchemy import  Column, Integer, String, Boolean, ForeignKey, DECIMAL, Date, SmallInteger, BLOB, Text, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

class Offices(Base):
    __tablename__ = 'offices'
    officeCode = Column(String, primary_key=True, index=True)
    city = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    addressLine1 = Column(String, nullable=True)
    addressLine2 = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    postalCode = Column(String, nullable=True)
    territory = Column(String, nullable=True)

class Employees(Base):
    __tablename__ = 'employees'
    username = Column(String, unique=True)
    employeeNumber = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, nullable=True)
    lastName = Column(String, nullable=True)
    extension = Column(String, nullable=True)
    email = Column(String, unique=True)
    officeCode = Column(String, ForeignKey("offices.officeCode"))
    reportsTo = Column(Integer, ForeignKey("employees.employeeNumber"))
    jobTitle = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)

     # ✅ Relationship: One Employee can have multiple Customers
    customers = relationship("Customers", back_populates="salesRep")

class Customers(Base):
    __tablename__ = 'customers'
    username = Column(String, unique=True)
    customerNumber = Column(Integer, primary_key=True, index=True)
    customerName = Column(String, nullable=True)
    contactLastName = Column(String, nullable=True)
    contactFirstName = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    addressLine1 = Column(String, nullable=True)
    addressLine2 = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    postalCode = Column(String, nullable=True)
    country = Column(String, nullable=True)
    salesRepEmployeeNumber = Column(Integer, ForeignKey("employees.employeeNumber"))
    creditLimit = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    hashed_password = Column(String)

    # ✅ Relationship: Customers have an Employee as a Sales Rep
    salesRep = relationship("Employees", back_populates="customers")

class ProductLines(Base):
    __tablename__ = 'productlines'
    productLine = Column(String, primary_key=True, index=True)
    textDescription = Column(String, nullable=True)
    htmlDescription =  Column(Text, nullable=True)
    image =  Column(BLOB, nullable=True)

class Products(Base):
    __tablename__ = 'products'
    productCode = Column(String, primary_key=True, index=True)
    productName = Column(String, nullable=True)
    productLine = Column(String, ForeignKey("productlines.productLine"))
    productScale = Column(String, nullable=True)
    productVendor = Column(String, nullable=True)
    productDescription = Column(Text, nullable=True)
    quantityInStock = Column(SmallInteger, nullable=True)
    buyPrice = Column(DECIMAL(10, 2), nullable=True)
    MSRP = Column(DECIMAL(10, 2), nullable=True)



class Orders(Base):
    __tablename__ = 'orders'
    orderNumber = Column(Integer, primary_key=True, index=True)
    orderDate = Column(Date)
    requiredDate = Column(Date)
    shippedDate = Column(Date)
    status = Column(String, nullable=True)
    comments = Column(String, nullable=True)
    customerNumber = Column(Integer, ForeignKey("customers.customerNumber"))

class OrderDetails(Base):
    __tablename__ = "orderdetails"
    __table_args__ = (
        PrimaryKeyConstraint('orderNumber', 'productCode'),
    )
    quantityOrdered = Column(Integer, nullable=True)
    priceEach = Column(DECIMAL(10, 2), nullable=True)
    orderDate = Column(Date)
    orderLineNumber = Column(SmallInteger)
    orderNumber = Column(Integer, ForeignKey("orders.orderNumber"))
    productCode = Column(String, ForeignKey("products.productCode"))

class Payments(Base):
    __tablename__ = "payments"
    customerNumber = Column(Integer, ForeignKey("customers.customerNumber"))
    checkNumber = Column(String, primary_key=True, index=True)
    paymentDate = Column(Date, nullable=True)
    amount = Column(DECIMAL(10, 2), nullable=True)

class Member(Base):
    __tablename__ = "members"
    member_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=True)  # nullable=True since original doesn't specify NOT NULL

class Committee(Base):
    __tablename__ = "committees"
    committee_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=True)














