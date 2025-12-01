# DTO para la detección de placas que se recibe en el endpoint
from pydantic import BaseModel
class DeteccionPlacaRequest(BaseModel):
    imagen_base64: str