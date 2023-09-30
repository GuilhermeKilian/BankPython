import datetime as dt
from dateutil import parser
from models import *
import sqlalchemy as db

class App():
    def __init__(self):
        super().__init__()
        
        self.config_session()
    
    def create_user(self, name, document, gender, birthday):
        customer = self.get_customer_by_document(document)
        if(customer):
            raise Exception("Duplicated_Document")
        
        newCustomer = Customer(name=name, document=document, gender=gender, birthday=birthday)
        self.session.add(newCustomer)
        self.session.commit()
        
    def open_account(self, document, accountType):
        customer = self.get_customer_by_document_or_error(document)
        
        bankAccountType = self.session.query(BankAccountType).where(BankAccountType.type == accountType).first()        
        
        if(bankAccountType is None):
            raise Exception("BankAccountType_NotFound")
        
        bankAccount = BankAccount(initial_balance=0, customer=customer, bankAccountType=bankAccountType)
        self.add_and_save(bankAccount)
        
    def deposit(self, document, value):
        bankAccount = self.get_bankaccount_by_document_or_error(document)        
        bankAccount.balance += value        
        movement = self.add_movement(bankAccount, value, "deposit")        
        self.add_and_save(movement)
            
    def withdraw(self, document, value):
        bankAccount = self.get_bankaccount_by_document_or_error(document)
        
        if(bankAccount.balance < value):
            raise Exception('Insuficient_Balance')
        
        if(bankAccount.bank_account_type.type is "investimento"):
            raise Exception('Invalid_Account')
        
        bankAccount.balance -= value        
        movement = self.add_movement(bankAccount=bankAccount, value=value, type="withdraw")
        self.add_and_save(movement)
            
    def apply_fee(self, document, value):
        bankAccount = self.get_bankaccount_by_document_or_error(document)
        
        if(bankAccount.bank_account_type.type is "corrente"):
            raise Exception("Invalid_Account")
        
        bankAccount.balance += bankAccount.balance * value
        movement = self.add_movement(bankAccount=bankAccount, value=value, type="fee")
        self.add_and_save(movement)
            
    def get_bankAccount_movement_by_document(self, document):
        return self.session.query(Movement).join(BankAccount).join(Customer).where(Customer.document == document).all()
            
    def add_movement(self, bankAccount, value, type):
        movementType = self.session.query(MovementType).where(MovementType.type == type).first()
        return Movement(date=dt.datetime.now(), value=value, movementType=movementType, bankAccount=bankAccount)
    
    def add_and_save(self, data):
        self.session.add(data)
        self.session.commit()
    
    def get_bankaccount_by_document_or_error(self, document):
        bankAccount = self.session.query(BankAccount).join(Customer).where(Customer.document == document).first()
        
        if(bankAccount is None):
            raise Exception("BankAccount_NotFound")
        
        return bankAccount
    
    def get_customer_by_document_or_error(self, document):
        
        customer = self.get_customer_by_document(document)
        
        if(customer is None):
            raise Exception("Customer_NotFound")
        
        return customer
    
    def get_customer_by_document(self, document):
        return self.session.query(Customer).where(Customer.document == document).first()
    
    def config_session(self):
        engine = self.get_engine()
        Session = orm.sessionmaker(bind=engine)
        self.session = Session()
        
    def get_engine():
        return db.create_engine('sqlite:///orm.db')