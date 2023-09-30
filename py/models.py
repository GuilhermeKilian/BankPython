import sqlalchemy.orm as orm
from sqlalchemy import Column, Integer, String, Float, Date,ForeignKey, create_engine

engine = create_engine('sqlite:///orm.db')
conn = engine.connect()
Base = orm.declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    gender = Column(String(255))
    document = Column(String(255))
    birthDay = Column(Date)
    
class BankAccountType(Base):
    __tablename__ = 'bankAccountType'
    id = Column(Integer, primary_key=True)
    type = Column(String(255))

class MovementType(Base):
    __tablename__ = 'movementType'
    id = Column(Integer, primary_key=True)
    type = Column(String(255))

class BankAccount(Base):
    __tablename__ = 'bankAccount'
    id = Column(Integer, primary_key=True)
    initial_balance = Column(Float)
    balance = Column(Float)
    bank_account_type_id = Column(Integer, ForeignKey(BankAccountType.id), nullable=False)        
    customer_id = Column(Integer, ForeignKey(Customer.id, ondelete="CASCADE"), nullable=False)
    
class Movement(Base):
    __tablename__ = 'movement'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    value = Column(Float)
    movement_type_id = Column(Integer, ForeignKey(MovementType.id), nullable=False)
    bank_account_id = Column(Integer, ForeignKey(BankAccount.id), nullable=False)
    
Customer.bank_account = orm.relationship(BankAccount)
    
Movement.movement_type = orm.relationship(MovementType)
Movement.bank_account = orm.relationship(BankAccount)

MovementType.movement = orm.relationship(Movement, uselist=True)

BankAccountType.bank_account = orm.relationship(BankAccount, uselist=True)

BankAccount.customer = orm.relationship(Customer)
BankAccount.bank_account_type = orm.relationship(BankAccountType)
BankAccount.movement = orm.relationship(Movement, uselist=True)

Base.metadata.create_all(engine)