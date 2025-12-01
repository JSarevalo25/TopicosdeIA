from typing import Optional
from pydantic import BaseModel
# DTO para la respuesta de la placa que se envio desde el servicio

class AlumnoResponse(BaseModel):
    matricula_id: str
    nombre: str
    ape_paterno: str
    ape_materno: str
    correo: str
    celular: str
    carrera: str
    num_incidencias: int


class PlacaResponse(BaseModel):
    placa_id: str
    marca: str
    modelo: str
    anio: int
    matricula_id: Optional[str] = None
    alumno: Optional[AlumnoResponse] = None

    class Config:
        orm_mode = True