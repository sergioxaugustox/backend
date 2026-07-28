from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Tarea(BaseModel):
    titulo: str
    descripcion: str
    hecho: bool

tareas=[]


@app.post("/tareas", status_code=201)
def crear_tareas(tarea:Tarea):
    tareas.append(tarea)
    return tarea
    
@app.delete("/tareas/{indice}")
def quitar_tarea(indice:int):
    if indice <0 or indice >= len(tareas):
     raise HTTPException(status_code=404, detail= "tarea no encontrada")
    tarea_borrada = tareas.pop(indice)
    return {"mensaje": "tarea borrada"}

@app.put("/tareas/{indice}")
def actualizar_tarea(indice: int, tarea_nueva: Tarea):
    if indice < 0 or indice >= len(tareas):
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    tareas[indice] = tarea_nueva
    return tareas[indice]