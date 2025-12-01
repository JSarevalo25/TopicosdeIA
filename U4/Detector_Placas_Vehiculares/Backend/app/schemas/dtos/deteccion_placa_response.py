#Dto para la respuesta de la deteccion de placas que se envia desde el servicio
from pydantic import BaseModel
class DeteccionPlacaResponse(BaseModel):
    texto_placa: str