# DTO para el correo request que se recibe en el endpont
from pydantic import BaseModel
class CorreoRequest(BaseModel):
    placa: str
    correo_destino: str
    latitud: float
    longitud: float
    image_base64: str
    nombre_estudiante: str
    apellidos_estudiante: str
    carrera_estudiante: str
    marca_modelo_año: str
    num_incidencias: int