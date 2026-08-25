
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal, Tarea as TareaDB, Insumo as InsumoDB, Precio as PrecioDB, Concepto as ConceptoDB, Composicion as ComposicionDB
from datetime import date 



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


class Insumo(BaseModel):
    nombre: str
    unidad: str
    tipo: str

class InsumoRespuesta(BaseModel):
    id: int
    nombre: str
    unidad: str
    tipo: str

    class Config:
        from_attributes = True

class Precio(BaseModel):
    insumo_id: int
    precio: float
    fecha_vigencia: date

class PrecioRespuesta(BaseModel):
    id: int
    insumo_id: int
    precio: float
    fecha_vigencia: date

    class Config:
        from_attributes = True

class Concepto(BaseModel):
    codigo: str
    descripcion: str
    unidad: str

class ConceptoRespuesta(BaseModel):
    id: int
    codigo: str
    descripcion: str
    unidad: str

    class Config:
        from_attributes = True

class Composicion(BaseModel):
    concepto_id: int
    insumo_id: int
    cantidad: float

class ComposicionRespuesta(BaseModel):
    id: int
    concepto_id: int
    insumo_id: int
    cantidad: float

    class Config:
        from_attributes = True

@app.get("/")
def read_root():
    return{"mensaje": "API de Tareas - FastAPI + PostgreSQL"}



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
def borrar_tarea(id: int, db: Session = Depends (get_db)):
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





@app.post("/insumos", status_code=201, response_model=InsumoRespuesta)
def nuevo_insumo(insumo: Insumo, db: Session = Depends(get_db)):
    nueva = InsumoDB(nombre=insumo.nombre, unidad=insumo.unidad, tipo=insumo.tipo)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@app.get("/insumos", response_model = list[InsumoRespuesta])
def listar_insumos(db:Session = Depends (get_db)):
    return db.query (InsumoDB).all()

@app.delete("/insumos/{id}")
def borrar_insumo(id: int, db: Session = Depends (get_db)):
    insumo= db.query(InsumoDB).filter(InsumoDB.id == id).first()
    if insumo is None:
        raise HTTPException (status_code=404, detail= "Insumo no encontrado")   
    db.delete(insumo)
    db.commit()
    return{"mensaje": "Insumo borrado"}



@app.put("/insumos/{id}", response_model=InsumoRespuesta)
def actualizar_insumo(id: int, insumo_nuevo:  Insumo, db: Session = Depends (get_db)):
    insumo=db.query(InsumoDB).filter(InsumoDB.id == id).first()
    if insumo is None:
        raise HTTPException (status_code=404, detail= "Insumo no encontrado")  
    insumo.nombre = insumo_nuevo.nombre
    insumo.unidad = insumo_nuevo.unidad
    insumo.tipo = insumo_nuevo.tipo
    db.commit()
    db.refresh(insumo)
    return insumo

@app.post("/precios", status_code=201, response_model=PrecioRespuesta)
def nuevo_precio(precio: Precio, db: Session = Depends(get_db)):
    nueva= PrecioDB(insumo_id= precio.insumo_id, precio= precio.precio, fecha_vigencia= precio.fecha_vigencia)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@app.get("/precios", response_model=list[PrecioRespuesta])
def listar_precios(db: Session = Depends(get_db)):
    return db.query(PrecioDB).all()

@app.post("/conceptos", status_code=201, response_model=ConceptoRespuesta)
def nuevo_concepto(concepto: Concepto, db: Session = Depends(get_db)):
    nueva= ConceptoDB(codigo= concepto.codigo, descripcion= concepto.descripcion, unidad = concepto.unidad)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@app.get("/conceptos", response_model=list[ConceptoRespuesta])
def listar_conceptos(db: Session = Depends(get_db)):
    return db.query(ConceptoDB).all()

@app.put("/conceptos/{id}", response_model=ConceptoRespuesta)
def actualizar_concepto(id: int, concepto_nuevo: Concepto, db: Session= Depends(get_db)):
    concepto= db.query(ConceptoDB).filter(ConceptoDB.id == id).first()
    if concepto is None:
        raise HTTPException(status_code=404, detail="Concepto no encontrado")
    concepto.codigo = concepto_nuevo.codigo
    concepto.descripcion = concepto_nuevo.descripcion
    concepto.unidad = concepto_nuevo.unidad
    db.commit()
    db.refresh(concepto)
    return concepto 

@app.delete("/conceptos/{id}")
def borrar_concepto(id: int, db: Session = Depends (get_db)):
    concepto= db.query(ConceptoDB).filter(ConceptoDB.id == id).first()
    if concepto is None:
        raise HTTPException (status_code=404, detail= "Concepto no encontrado")   
    db.delete(concepto)
    db.commit()
    return{"mensaje": "concepto borrado"}

@app.post("/composicion", status_code=201, response_model=ComposicionRespuesta)
def nuevo_composicion(composicion: Composicion, db: Session = Depends(get_db)):
    nueva= ComposicionDB(concepto_id= composicion.concepto_id, insumo_id= composicion.insumo_id, cantidad= composicion.cantidad)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@app.get("/composicion", response_model=list[ComposicionRespuesta])
def listar_composicion(db: Session = Depends(get_db)):
    return db.query(ComposicionDB).all()
