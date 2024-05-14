from datetime import date
from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base, engine

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


    carts = relationship("Cart", back_populates="users")


class Tool(Base):
    __tablename__ = 'tools'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String, index=True)
    category = Column(String, index=True)
    price = Column(Float, index=True)
    stock = Column(Integer, index=True)

    tools_in_cart = relationship("ToolsInCart", back_populates="tool")


class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    #date = Column(Date)
    total_price = Column(Float)

    
    users = relationship("User", back_populates="carts")
    tools_in_cart = relationship("ToolsInCart", back_populates="cart")

    def calculate_total_price(self):
        total_price = 0.0
        for item in self.tools_in_cart:
            total_price += item.tool.price * item.quantity
        return total_price


class ToolsInCart(Base):
    __tablename__ = 'tools_in_cart'
    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, ForeignKey("tools.id"))
    cart_id = Column(Integer, ForeignKey("carts.id"))
    quantity = Column(Integer)

    tool = relationship("Tool", back_populates="tools_in_cart")
    cart = relationship("Cart", back_populates="tools_in_cart")

Base.metadata.create_all(bind=engine)