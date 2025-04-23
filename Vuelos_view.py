from sqlalchemy.orm import Session
from models import VueloDB
from schemas import Vuelo
from fastapi import HTTPException

class ColaVuelos:
    def __init__(self, db: Session):
        self.db = db
        self.vuelos = self.db.query(VueloDB).order_by(VueloDB.id).all()  # Cargar vuelos desde DB

    def insertar_al_final(self, vuelo: Vuelo):
        """Inserta un vuelo en la cola respetando la prioridad."""
        db_vuelo = VueloDB(**vuelo.dict())
        self.db.add(db_vuelo)
        self.db.commit()
        self.db.refresh(db_vuelo)

        # Verificar si el vuelo tiene prioridad
        if vuelo.prioridad:  # Si el vuelo tiene prioridad, lo insertamos al principio
            self.vuelos.insert(0, db_vuelo)
        else:  # Si no tiene prioridad, se agrega al final
            self.vuelos.append(db_vuelo)

        return db_vuelo

    def obtener_primero(self):
        """Obtiene el primer vuelo en la cola (sin eliminar)."""
        if not self.vuelos:
            raise HTTPException(status_code=404, detail="No hay vuelos")
        return self.vuelos[0]

    def obtener_ultimo(self):
        """Obtiene el último vuelo en la cola (sin eliminar)."""
        if not self.vuelos:
            raise HTTPException(status_code=404, detail="No hay vuelos")
        return self.vuelos[-1]

    def longitud(self):
        """Retorna la cantidad total de vuelos en la cola."""
        return len(self.vuelos)

    def obtener_lista_completa(self):
        """Retorna la lista completa de vuelos."""
        return self.vuelos

    def insertar_en_posicion(self, vuelo: Vuelo, posicion: int):
        """Inserta un vuelo en una posición específica (por índice)."""
        db_vuelo = VueloDB(**vuelo.dict())
        self.db.add(db_vuelo)
        self.db.commit()
        self.db.refresh(db_vuelo)
        self.vuelos.insert(posicion, db_vuelo)
        return db_vuelo

    def extraer_de_posicion(self, posicion: int):
        """Elimina y retorna el vuelo en la posición especificada."""
        if posicion < 0 or posicion >= len(self.vuelos):
            raise HTTPException(status_code=400, detail="Posición inválida")
        vuelo = self.vuelos.pop(posicion)
        self.db.delete(vuelo)
        self.db.commit()
        return vuelo

    def ordenar_vuelos(self):
        """Ordenar los vuelos para que los de prioridad estén primero, respetando el orden de llegada."""
        # Dividir los vuelos en dos listas: uno con prioridad y otro sin
        vuelos_con_prioridad = [vuelo for vuelo in self.vuelos if vuelo.prioridad]
        vuelos_sin_prioridad = [vuelo for vuelo in self.vuelos if not vuelo.prioridad]

        # Los vuelos con prioridad deben ir primero, seguidos de los vuelos sin prioridad
        self.vuelos = vuelos_con_prioridad + vuelos_sin_prioridad
