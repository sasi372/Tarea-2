from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import Vuelo
from cola import ColaVuelos

app = FastAPI()

@app.post("/vuelos/", response_model=Vuelo)
def crear_vuelo(vuelo: Vuelo, es_emergencia: bool = False, db: Session = Depends(get_db)):
    cola = ColaVuelos(db)
    return cola.agregar_vuelo(vuelo, es_emergencia)

@app.get("/vuelos/proximo", response_model=Vuelo)
def obtener_proximo_vuelo(db: Session = Depends(get_db)):
    cola = ColaVuelos(db)
    return cola.obtener_proximo()

@app.delete("/vuelos/proximo", response_model=Vuelo)
def despegar_proximo_vuelo(db: Session = Depends(get_db)):
    cola = ColaVuelos(db)
    return cola.despegar_proximo()

@app.get("/vuelos/", response_model=list[Vuelo])
def listar_vuelos(db: Session = Depends(get_db)):
    cola = ColaVuelos(db)
    return cola.listar_vuelos()

@app.get("/vuelos/total", response_model=int)
def total_vuelos(db: Session = Depends(get_db)):
    cola = ColaVuelos(db)
    return cola.total_vuelos()
