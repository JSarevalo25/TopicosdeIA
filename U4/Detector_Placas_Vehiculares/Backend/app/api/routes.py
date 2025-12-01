from fastapi import APIRouter, HTTPException
from app.schemas.dtos.deteccion_placa_request import DeteccionPlacaRequest
from app.schemas.dtos.deteccion_placa_response import DeteccionPlacaResponse
from app.services.placa_service import buscar_por_placa, detectar_placa
from app.schemas.dtos.placa_response import PlacaResponse

router = APIRouter()

# Endpoint para obtener la información de una placa vehicular
# Recibe como parámetro la placa en la URL
# Retorna un PlacaResponse con la información del vehiculo y su dueño (estudiante)
# {
#   "placa_id": "ABC123",
#   "marca": "Toyota",
#   "modelo": "Corolla",
#   "anio": 2020,
#   "matricula_id": "20204567",
#   "alumno": {
#     "matricula_id": "20204567",
#     "nombre": "Juan",
#     "ape_paterno": "Pérez",
#     "ape_materno": "López",
#     "correo": "juan.perez@universidad.mx",
#     "celular": "6671234567",
#     "carrera": "Ingeniería en Sistemas",
#     "num_incidencias": 2
#   }
# }

@router.get("/{placa}", response_model=PlacaResponse)
async def obtener_info_placa(placa: str):
    print(placa)
    data = await buscar_por_placa(placa)
    if data is None:
        raise HTTPException(status_code=404, detail="Placa no encontrada")

    return data  

# Endpoint para detectar la placa en una imagen enviada en base64
# Recibe un DeteccionPlacaRequest con la imagen en base64
# Json de DeteccionPlacaRequest:
# {
#   "imagen_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
# }
# Retorna un DeteccionPlacaResponse con el texto de la placa detectada
# Json de DeteccionPlacaResponse:
# {
#   "texto_placa": "ABC1234"
#}
@router.post("/detectar-placa", response_model = DeteccionPlacaResponse)
async def procesodetectar_placa(placa_request: DeteccionPlacaRequest):
    data = await detectar_placa(placa_request.imagen_base64)
    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"])

    return data  
