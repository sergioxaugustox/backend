# API de Tareas

API REST para gestionar tareas con operaciones CRUD.

## Tecnologías

- Python / FastAPI
- PostgreSQL (Supabase)
- SQLAlchemy
- Pydantic

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/tareas` | Crea una tarea |
| GET | `/tareas` | Lista todas las tareas |
| PUT | `/tareas/{id}` | Actualiza una tarea |
| DELETE | `/tareas/{id}` | Elimina una tarea |

## Cómo correr

1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar el entorno: `venv\Scripts\activate`
4. Instalar dependencias: `pip install -r requirements.txt`
5. Configurar el archivo `.env` con tu `DATABASE_URL`
6. Arrancar el servidor: `fastapi dev main.py`
