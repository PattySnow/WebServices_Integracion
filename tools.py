from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from requests import Session
from config.db import SessionLocal, engine, Base
from models.model import Tool as ModelTool

app = FastAPI(
    title='FERREMAX-MODULO HERRAMIENTAS',
    version='0.0.1',
)

Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(BaseModel):
    email: str
    password: str

class ToolRequest(BaseModel):
    name: str = Field(default='Nombre de la herramienta', max_length=50)
    brand: str = Field(default='Marca')
    category: str = Field(default='Categoria')
    price: float = Field(default=0.0)
    stock: int = Field

@app.get('/', tags=['Home'])
def read_root():
    return HTMLResponse('<h2> Bienvenido a Ferremax </h2>')

@app.post('/tools', tags=['Herramientas'], status_code=201)
def create_tool(tool: ToolRequest, db: Session = Depends(get_db)):
    new_tool = ModelTool(name=tool.name, brand=tool.brand, category=tool.category, price=tool.price, stock=tool.stock)
    db.add(new_tool)
    db.commit()
    
    # Convertir el objeto new_tool en un diccionario
    tool_dict = {
        "id": new_tool.id,
        "name": new_tool.name,
        "brand": new_tool.brand,
        "category": new_tool.category,
        "price": new_tool.price,
        "stock": new_tool.stock
    }
    
    return JSONResponse(status_code=201, content={'Message': 'Nueva herramienta guardada', 'Tool': tool_dict})


@app.get('/tools', tags=['Herramientas'])
def get_tools():
    db = SessionLocal()
    data = db.query(ModelTool).all()
    return JSONResponse(content=jsonable_encoder(data))

@app.get('/tools/{id}', tags=['Herramientas'], status_code=200)
def get_tool(id: int):
    db = SessionLocal()
    data = db.query(ModelTool).filter(ModelTool.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return JSONResponse(status_code=200, content=jsonable_encoder(data))



@app.put('/tools/{id}', tags=['Herramientas'], status_code=200)
def update_tool(id: int, tool: ToolRequest):
    db = SessionLocal()
    data = db.query(ModelTool).filter(ModelTool.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    data.name = tool.name
    data.brand = tool.brand
    data.category = tool.category
    data.price = tool.price
    data.stock = tool.stock
    db.commit()
    return JSONResponse(status_code=200, content={'Message': 'Se ha modificado la herramienta'})

@app.delete('/tools/{id}', tags=['Herramientas'], status_code=200)
def delete_tool(id: int):
    db = SessionLocal()
    data = db.query(ModelTool).filter(ModelTool.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    db.delete(data)
    db.commit()
    return JSONResponse(status_code=200, content={'Message': 'Se ha eliminado la herramienta'})
