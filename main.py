
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class Tarea(BaseModel):
    titulo: str
    descripcion: str
    hecho: bool

tareas = []


app = FastAPI()
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


@app.post ("/tareas" , status_code=201)
def crear_tarea(tarea : Tarea ):
    tareas .append( tarea)
    return tarea 

@app.get("/tareas")
def listar_tareas():
    return tareas


@app.delete("/tareas/{indice}")
def borrar_tareas(indice: int):
    tareas.pop(indice)          
    return {"mensaje": "tarea borrada"}    