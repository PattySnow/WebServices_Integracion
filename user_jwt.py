from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from config.db import SessionLocal, engine, Base
from models.model import User as ModelUser
from pydantic import BaseModel, Field
import bcrypt



from sqlalchemy.orm import Session



app = FastAPI(
    title='Modulo Usuarios',
    version='0.0.1',
)

Base.metadata.create_all(bind=engine)



class User(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
  


@app.get('/', tags=['Home'])
def read_root():
    return HTMLResponse('<h2> Bienvenido al Modulo Usuarios </h2>')


@app.post('/users', tags=['Usuarios'])
def create_user(user: User):
    db = SessionLocal()
    hashed_password = bcrypt.hashpw(user.hashed_password.encode('utf-8'), bcrypt.gensalt())
    db_user = ModelUser(id= user.id, username=user.username, email=user.email, hashed_password=hashed_password.decode('utf-8'))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




@app.get('/users', tags=['Usuarios'])
def get_user(id: int):
    db = SessionLocal()
    data = db.query(ModelUser).filter(ModelUser.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return JSONResponse(status_code=200, content=jsonable_encoder(data))



@app.get('/users/{email}', tags=['Usuarios'])
def get_user_by_email(email: str):
    db = SessionLocal()
    user = db.query(ModelUser).filter(ModelUser.email == email).first()
    db.close()
    return user


@app.put('/users/{email}', tags=['Usuarios'])
def update_user(email: str, user: User):
    db = SessionLocal()
    data = db.query(ModelUser).filter(ModelUser.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    data.username = user.username
    data.email = user.email
    data.hashed_password = user.hashed_password
    db.commit()
    db.close()
    return JSONResponse(content={'Message': 'se ha modificado el usuario'})


@app.delete('/users/{email}', tags=['Usuarios'])
def delete_user(email: str):
    db = SessionLocal()
    user = db.query(ModelUser).filter(ModelUser.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
    db.close()
    return {"message": "Usuario eliminado exitosamente"}
