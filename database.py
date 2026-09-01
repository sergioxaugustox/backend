import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Date

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descripcion = Column(String)
    hecho = Column(Boolean, default=False)

class Insumo(Base):
    __tablename__ = "insumos" 
    id = Column(Integer,primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    unidad = Column(String, nullable=False)   
    tipo = Column(String, nullable=False)

class Concepto(Base):
    __tablename__ = "conceptos"
    id = Column(Integer,primary_key=True, index=True )
    codigo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    unidad = Column(String, nullable=False)

class Composicion(Base):
    __tablename__ = "composicion"
    id = Column(Integer, primary_key=True, index=True)
    concepto_id = Column(Integer, ForeignKey("conceptos.id"), nullable=False)
    insumo_id = Column(Integer, ForeignKey("insumos.id"), nullable=False)
    cantidad = Column(Float, nullable=False)

class Precio(Base):
    __tablename__ ="precios"
    id = Column(Integer, primary_key=True, index=True)
    insumo_id = Column(Integer, ForeignKey("insumos.id"), nullable=False)
    precio = Column(Float, nullable=False)
    fecha_vigencia = Column(Date,nullable=False)

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)



Base.metadata.create_all(bind=engine)