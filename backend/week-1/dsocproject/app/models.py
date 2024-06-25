# models.py

from sqlalchemy import (
    Column, String, Text, DECIMAL, Integer, Boolean,
    CheckConstraint, ForeignKey, TIMESTAMP, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import re
import datetime

Base = declarative_base()

# InventoryItem Model
class InventoryItem(Base):
    __tablename__ = 'inventoryitem'
    
    Item_SKU = Column(String, primary_key=True)
    Item_Name = Column(String, nullable=False)
    Item_Description = Column(Text)
    Item_Price = Column(DECIMAL, nullable=False)
    Item_Qty = Column(Integer, nullable=False)
    Category_ID = Column(Integer, ForeignKey('inventoryitem.Item_SKU'), nullable=True)gt
    
    parent_category = relationship('InventoryItem', remote_side=[Item_SKU], backref='subcategories')

    __table_args__ = (
        CheckConstraint('Item_Price >= 0', name='check_item_price_non_negative'),
        CheckConstraint('Item_Qty >= 0', name='check_item_qty_non_negative'),
    )

    def validate(self):
        if self.Item_Price < 0:
            raise ValueError("Item_Price must be non-negative")
        if self.Item_Qty < 0:
            raise ValueError("Item_Qty must be non-negative")

    @staticmethod
    def total_inventory_value(session):
        result = session.query(InventoryItem).all()
        total_value = sum(item.Item_Price * item.Item_Qty for item in result)
        return total_value

    def __repr__(self):
        return f"<InventoryItem(Item_SKU='{self.Item_SKU}', Item_Name='{self.Item_Name}')>"

# Customer Model
class Customer(Base):
    __tablename__ = 'customer'
    
    c_ID = Column(Integer, primary_key=True, autoincrement=True)
    c_name = Column(String, nullable=False)
    c_email = Column(String, nullable=False, unique=True)
    c_contact = Column(String)
    
    def validate(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.c_email):
            raise ValueError("Invalid email format")

    def get_transactions(self, session):
        return session.query(Transaction).filter(Transaction.c_ID == self.c_ID).all()

    def __repr__(self):
        return f"<Customer(c_ID='{self.c_ID}', c_name='{self.c_name}')>"

# Staff Model
class Staff(Base):
    __tablename__ = 'staff'
    
    s_ID = Column(Integer, primary_key=True, autoincrement=True)
    s_name = Column(String, nullable=False)
    s_email = Column(String, nullable=False, unique=True)
    s_isAdmin = Column(Boolean, default=False)
    s_contact = Column(String)
    
    def validate(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.s_email):
            raise ValueError("Invalid email format")

    def __repr__(self):
        return f"<Staff(s_ID='{self.s_ID}', s_name='{self.s_name}')>"

# Transaction Model
class Transaction(Base):
    __tablename__ = 'transaction'
    
    t_ID = Column(Integer, primary_key=True, autoincrement=True)
    c_ID = Column(Integer, ForeignKey('customer.c_ID'), nullable=False)
    s_ID = Column(Integer, ForeignKey('staff.s_ID'), nullable=False)
    Item_SKU = Column(String, ForeignKey('inventoryitem.Item_SKU'), nullable=False)
    t_date = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    t_amount = Column(DECIMAL, nullable=False)
    t_category = Column(String)
    
    customer = relationship("Customer")
    staff = relationship("Staff")
    item = relationship("InventoryItem")
    
    __table_args__ = (
        CheckConstraint('t_amount >= 0', name='check_transaction_amount_non_negative'),
    )

    def validate(self):
        if self.t_amount < 0:
            raise ValueError("t_amount must be non-negative")

    def __repr__(self):
        return f"<Transaction(t_ID='{self.t_ID}', t_amount='{self.t_amount}')>"

# Database setup for PostgreSQL
def init_db():
    # Replace these values with your PostgreSQL configuration
    user = 'postgres'
    password = 'mypassword'
    host = 'localhost'
    port = '5432'
    database = 'mydatabase'
    
    DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

# Seed data function
def seed_data(session):
    # Inventory items
    items = [
        InventoryItem(Item_SKU='1001', Item_Name='Laptop', Item_Price=999.99, Item_Qty=10),
        InventoryItem(Item_SKU='1002', Item_Name='Keyboard', Item_Price=49.99, Item_Qty=100),
        InventoryItem(Item_SKU='1003', Item_Name='Mouse', Item_Price=25.99, Item_Qty=150),
    ]
    for item in items:
        item.validate()
        session.add(item)

    # Customers
    customers = [
        Customer(c_name='Alice Smith', c_email='alice@example.com', c_contact='555-1234'),
        Customer(c_name='Bob Jones', c_email='bob@example.com', c_contact='555-5678'),
    ]
    for customer in customers:
        customer.validate()
        session.add(customer)

    # Staff
    staff_members = [
        Staff(s_name='Charlie Admin', s_email='charlie@example.com', s_isAdmin=True, s_contact='555-0001'),
        Staff(s_name='David Employee', s_email='david@example.com', s_isAdmin=False, s_contact='555-0002'),
    ]
    for staff in staff_members:
        staff.validate()
        session.add(staff)

    # Transactions
    transactions = [
        Transaction(c_ID=1, s_ID=1, Item_SKU='1001', t_amount=999.99, t_category='Sale'),
        Transaction(c_ID=2, s_ID=2, Item_SKU='1002', t_amount=49.99, t_category='Sale'),
    ]
    for transaction in transactions:
        transaction.validate()
        session.add(transaction)

    session.commit()

# Example usage
if __name__ == '__main__':
    Session = init_db()
    session = Session()
    
    # Seed the database
    seed_data(session)

    # Example operations
    print("Total inventory value:", InventoryItem.total_inventory_value(session))
    customer = session.query(Customer).filter_by(c_name='Alice Smith').first()
    print("Transactions for Alice Smith:", customer.get_transactions(session))

'''InventoryItem:
Fields: Item_SKU, Item_Name, Item_Description, Item_Price, Item_Qty, Category_ID
Relationships: Self-referential parent-child hierarchy via Category_ID
Methods: validate(), total_inventory_value()
Customer:
Fields: c_ID, c_name, c_email, c_contact
Relationships: Transactions via foreign key in Transaction
Methods: validate(), get_transactions()
Staff:
Fields: s_ID, s_name, s_email, s_isAdmin, s_contact
Methods: validate()
Transaction:
Fields: t_ID, c_ID, s_ID, Item_SKU, t_date, t_amount, t_category
Relationships: Customer, Staff, InventoryItem via foreign keys
Methods: validate()'''