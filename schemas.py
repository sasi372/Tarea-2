from pydantic import BaseModel

class Vuelo(BaseModel):
    codigo: str
    estado: str
    hora: str
    origen: str
    destino: str
    prioridad: bool = False

    class Config:
        orm_mode = True
