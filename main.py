
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from database import engine, Base
from database import SessionLocal
from sqlalchemy.orm import Session
from database import Tarea as TareaDB



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


            
app = FastAPI()

class Tarea(BaseModel):
    titulo: str
    descripcion: str
    hecho: bool

class TareaRespuesta(BaseModel):
    id: int
    titulo: str
    descripcion: str
    hecho: bool

    class Config:
        from_attributes = True    





@app.get("/")
def read_root():
    return{"mensaje": "hola"}


@app.get("/saludo/{nombre}")
def saludar(nombre):
    return{"mensaje": f"hola {nombre} que tal tu dia"}

@app.get("/buscar")
def buscando_en(ciudad):
    return{"buscando en": f"la ciudad de {ciudad}"}


@app.get("/usuarios/{user_id}/productos")
def funcion(user_id, categoria):
    return{"usuario": user_id,  "categoria": categoria }


@app.post("/tareas", status_code=201, response_model=TareaRespuesta)
def crear_tarea(tarea : Tarea, db: Session = Depends (get_db) ):
    nueva = TareaDB(titulo = tarea.titulo, descripcion = tarea.descripcion, hecho = tarea.hecho)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva 

@app.get("/tareas", response_model=list[TareaRespuesta])
def listar_tareas(db: Session = Depends(get_db)):
    return db.query(TareaDB).all()


@app.delete("/tareas/{id}")
def borrar_tareas(id: int, db: Session = Depends (get_db)):
    tarea = db.query(TareaDB).filter(TareaDB.id == id).first()
    if tarea is None:
        raise HTTPException(status_code=404, detail = "Tarea no encontrada")
    db.delete(tarea)
    db.commit()
    return {"mensaje": "tarea borrada"}    

@app.put("/tareas/{id}, response_model=TareaRespuesta")
def actualizar_tarea(id: int, tarea_nueva: Tarea, db: Session = Depends(get_db)):
    tarea = db.query(TareaDB).filter(TareaDB.id == id) .first()
    if tarea is None:
        raise HTTPException(status_code=404, detail = "tarea no encontrada")
    tarea.titulo = tarea_nueva.titulo
    tarea.descripcion = tarea_nueva.descripcion
    tarea.hecho = tarea_nueva.hecho
    db.commit()
    db.refresh(tarea)
    return tarea



Base.metadata.create_all(bind=engine)
