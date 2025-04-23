from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VueloDB(Base):
    __tablename__ = "vuelos"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True)
    estado = Column(String)
    hora = Column(String)
    origen = Column(String)
    destino = Column(String)
    prioridad = Column(Boolean)
