from sqlalchemy import create_engine,Table,Column,MetaData,Integer,String,ForeignKey,Date,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, backref, relationship
import os

#if os.path.exists("webProject.db"):
    #os.remove("webProject.db")

engine = create_engine('sqlite:///webProject.db')
Session = sessionmaker()
Base = declarative_base(bind=engine)
countCustomer = 0

class Admin(Base):
     __tablename__ = "Admin"
     Login = Column(String, nullable = False,primary_key = True)
     Password = Column(String, nullable = False)
     def __init__(self, Login, Password):
          self.Login = Login
          self.Password = Password

     def __repr__(self):
          return self.Login + " " + self.Password + " " + self.FirstName + " " +self.SecondName 


class User(Base):
     __tablename__ = "Users"
     Login = Column(String, nullable = False,primary_key = True)
     Password = Column(String, nullable = False)
     FirstName = Column(String, nullable = False)
     SecondName = Column(String, nullable = False)
     Mail = Column(String, nullable = False)
     Tel = Column(String, nullable = False)
     def __init__(self, Login, Password, FirstName, SecondName, Mail, Tel):
          self.Login = Login
          self.Password = Password
          self.FirstName = FirstName
          self.SecondName = SecondName
          self.Mail = Mail
          self.Tel = Tel

     def __repr__(self):
          return self.Login + " " + self.Password + " " + self.FirstName + " " +self.SecondName 

class Product(Base):
     __tablename__= "Product"
     id = Column(Integer, nullable= False, primary_key = True)
     Name = Column(String, nullable=False)
     Cost = Column(String, nullable = False)
     Picture = Column(String, nullable = False)
     def __init__(self, Name, Cost, Picture):
          super(Product, self).__init__()
          self.Name = Name
          self.Cost = Cost
          self.Picture = Picture

     def __repr__(self):
          return self.Name + " " + self.Picture + " " + self.Cost
          

class TempOrder(Base):
     __tablename__= "TempOrder"
     id = Column(Integer, nullable = False, primary_key = True)
     IdCustomer = Column(Integer, nullable = False)
     IdProduct = Column(Integer, nullable = False)
     Count = Column(Integer, nullable = False)
     def __init__(self, IdCustomer, IdProduct, Count):
          super(TempOrder, self).__init__()
          self.IdCustomer = IdCustomer
          self.IdProduct = IdProduct
          self.Count = Count

     def __repr__(self):
          return str(self.IdProduct) + " " + str(self.IdCustomer) + " " + str(self.Count)
          
class Order(Base):
     __tablename__= "Order"
     id = Column(Integer, nullable = False, primary_key = True)
     IdCustomer = Column(String, nullable = False)
     IdProduct = Column(Integer, nullable = False)
     Count = Column(Integer, nullable = False)
     def __init__(self, IdCustomer, IdProduct, Count):
          super(Order, self).__init__()
          self.IdCustomer = IdCustomer
          self.IdProduct = IdProduct
          self.Count = Count

     def __repr__(self):
          return str(self.IdProduct) + " " + str(self.IdCustomer) + " " + str(self.Count)