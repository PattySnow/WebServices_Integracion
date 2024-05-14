from fastapi import Depends, HTTPException, FastAPI, Path
from sqlalchemy.orm import Session
from config.db import Base, SessionLocal, engine
from models.model import User, Tool, Cart as CartModel, ToolsInCart
from typing import List, Optional
from pydantic import BaseModel



app = FastAPI()

Base.metadata.create_all(bind=engine)



class Cart(BaseModel):
    user_id: int
    cart_id: int
    tool_id: int
    quantity: int
    # date: date

class CartUpdate(BaseModel):
    cart_id: Optional[int] = None
    tool_id: Optional[int] = None
    quantity: Optional[int] = None
    


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/cart/", response_model=None)
def add_item_to_cart(tool_id: int, quantity: int, user_id: int, db: Session = Depends(get_db)):
    """
    Agregar items al carrito
    """
    # Verificar si la herramienta existe
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Herramienta no encontrada")

    # Crear el artículo en el carrito
    cart_item = ToolsInCart(
        tool_id=tool_id,
        quantity=quantity
    )
    db.add(cart_item)
    db.commit()

    # Obtener el carrito del usuario
    cart = db.query(CartModel).filter(CartModel.user_id == user_id).first()

    if not cart:
        # Si el usuario no tiene un carrito, puedes crear uno aquí
        cart = CartModel(user_id=user_id, total_price=0)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Agregar el artículo al carrito
    cart.tools_in_cart.append(cart_item)

    # Llamar a la función para calcular el precio total del carrito
    cart.calculate_total_price()

    # Asignar el precio total calculado al atributo total_price
    cart.total_price = cart.calculate_total_price()


    db.commit()

    return {"message": "Herramienta agregada exitosamente"}


@app.get("/cart/{cart_id}", response_model=None)
def get_user_cart(cart_id: int, db: Session = Depends(get_db)):
    """
    Get user's cart
    """
    cart_items = db.query(ToolsInCart).filter(
        ToolsInCart.cart_id == cart_id).all()
    return cart_items


@app.put("/cart/{cart_id}")
def update_cart_item(cart_id: int , cart_update: CartUpdate, db: Session = Depends(get_db)):
    """
    Actualizar carrito
    """
    db_cart_item = db.query(ToolsInCart).filter(
        ToolsInCart.id == cart_id).first()
    if not db_cart_item:
        raise HTTPException(status_code=404, detail="No se encontro el item en el carrito")

    for var, value in vars(cart_update).items():
        # Verificar si la propiedad existe en el modelo ToolsInCart
        if hasattr(db_cart_item, var):
            setattr(db_cart_item, var, value) if value is not None else None
    db.commit()
    db.refresh(db_cart_item)

    # Obtener el carrito asociado al artículo y actualizar el precio total
    cart = db.query(CartModel).filter(
        CartModel.id == db_cart_item.cart_id).first()
    if cart:
         # Llamar a la función para calcular el precio total del carrito
        cart.calculate_total_price()

        # Asignar el precio total calculado al atributo total_price
        cart.total_price = cart.calculate_total_price()
        db.commit()

    return {"message": "Carrito actualizado existosamente"}


@app.delete("/cart/{cart_id}/{tool_id}")
def remove_item_from_cart(cart_id: int, tool_id: int = Path(...), db: Session = Depends(get_db)):
    """
    Remover herramientas del carrito
    """
    db_cart_item = db.query(ToolsInCart).filter(
        ToolsInCart.cart_id == cart_id, 
        ToolsInCart.tool_id == tool_id
    ).first()
    if not db_cart_item:
        raise HTTPException(status_code=404, detail="No se encontro el item en el carrito")
    db.delete(db_cart_item)
    db.commit()

    # Obtener el carrito asociado al artículo y actualizar el precio total
    cart = db.query(CartModel).filter(
        CartModel.id == cart_id).first()
    if cart:
        cart.calculate_total_price()

        # Asignar el precio total calculado al atributo total_price
        cart.total_price = cart.calculate_total_price()
        
        db.commit()

    return {"message": "item eliminado del carrito exitosamente"}
    