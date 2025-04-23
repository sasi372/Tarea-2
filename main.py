from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, VueloDB
from schemas import Vuelo
from Vuelos_view import ColaVuelos

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/vuelos/", response_model=Vuelo)
def crear_vuelo(vuelo: Vuelo, db: Session = Depends(get_db)):
    cola = ColaVuelos(db)
    return cola.insertar_al_final(vuelo)

@app.get("/vuelos/primero", response_model=Vuelo)
def obtener_primero(db: Session = Depends(get_db)):
    cola = ColaVuelos(db)
    return cola.obtener_primero()

@app.get("/vuelos/ultimo", response_model=Vuelo)
def obtener_ultimo(db: Session = Depends(get_db)):
    cola = ColaVuelos(db)
    return cola.obtener_ultimo()

@app.get("/vuelos/total", response_model=int)
def total_vuelos(db: Session = Depends(get_db)):
    cola = ColaVuelos(db)
    return cola.longitud()

@app.get("/vuelos/", response_model=list[Vuelo])
def obtener_lista_completa(db: Session = Depends(get_db)):
    cola = ColaVuelos(db)
    cola.ordenar_vuelos()  # Asegurarse de ordenar la cola antes de retornar
    return cola.obtener_lista_completa()

@app.post("/vuelos/posicion/{posicion}", response_model=Vuelo)
def insertar_en_posicion(vuelo: Vuelo, posicion: int, db: Session = Depends(get_db)):
    cola = ColaVuelos(db)
    return cola.insertar_en_posicion(vuelo, posicion)

@app.delete("/vuelos/posicion/{posicion}", response_model=Vuelo)
def extraer_de_posicion(posicion: int, db: Session = Depends(get_db)):
    cola = ColaVuelos(db)
    return cola.extraer_de_posicion(posicion)
