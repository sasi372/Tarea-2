from Linked_Queue import LinkedQueue
from models import VueloDB
from schemas import Vuelo
from fastapi import HTTPException
from sqlalchemy.orm import Session

class ColaVuelos:
    def __init__(self, db: Session):
        self.db = db
        self.cola = LinkedQueue()
        self._cargar_vuelos()

    def _cargar_vuelos(self):
        vuelos = self.db.query(VueloDB).order_by(VueloDB.id).all()
        for vuelo in vuelos:
            self.cola.enqueue(vuelo)

    def agregar_vuelo(self, vuelo: Vuelo, es_emergencia: bool = False):
        db_vuelo = VueloDB(**vuelo.dict())
        self.db.add(db_vuelo)
        self.db.commit()
        self.db.refresh(db_vuelo)

        if es_emergencia:
            # No hay inserción al frente en LinkedQueue, así que reconstruimos
            aux_cola = LinkedQueue()
            aux_cola.enqueue(db_vuelo)
            while not self.cola.is_empty():
                aux_cola.enqueue(self.cola.dequeue())
            self.cola = aux_cola
        else:
            self.cola.enqueue(db_vuelo)

        return db_vuelo

    def obtener_proximo(self):
        if self.cola.is_empty():
            raise HTTPException(status_code=404, detail="No hay vuelos en la cola")
        return self.cola.first()

    def despegar_proximo(self):
        if self.cola.is_empty():
            raise HTTPException(status_code=404, detail="No hay vuelos en la cola")
        vuelo = self.cola.dequeue()
        self.db.delete(vuelo)
        self.db.commit()
        return vuelo

    def listar_vuelos(self):
        # Recorremos sin modificar la cola real
        vuelos = []
        aux_cola = LinkedQueue()
        while not self.cola.is_empty():
            vuelo = self.cola.dequeue()
            vuelos.append(vuelo)
            aux_cola.enqueue(vuelo)
        self.cola = aux_cola
        return vuelos

    def total_vuelos(self):
        return len(self.cola)
