from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#This is for SQLITE database connection
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False})


# Postgres Database connection
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost:5432/TodoApplicationDatabase'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# MySQl Database Connection
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:root@127.0.0.1:3306/classicmodels'
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



