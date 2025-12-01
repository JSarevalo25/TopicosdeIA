from fastapi import APIRouter, HTTPException
from app.services.correo_service import post_correo
from app.schemas.dtos.correo_request import CorreoRequest
router = APIRouter()

# Endpoint para enviar correo
# Aqui solicita un CorreoRequest
# de formato json:
# {
#   "placa": "ABC1234",
#   "correo_destino": "ejemplo@correo.com",
#   "latitud": 24.8091,
#   "longitud": -107.3940,
#   "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...", 
#   "nombre_estudiante": "Juan",
#   "apellidos_estudiante": "Pérez López",
#   "carrera_estudiante": "Ingeniería en Sistemas",
#   "marca_modelo_año": "Toyota Corolla 2018",
#   "num_incidencias": 3
# }

# Enviara dos correos (uno a la institucion y otro al estudiante)
# con la informacion del vehiculo mal estacionado
# y aumentara el numero de incidencias del estudiante en la BD
# y retornara un mensaje de exito
@router.post("/enviar-correo")
async def enviar_correo(correo_request: CorreoRequest):
    # validar que se reciban los parametros necesarios
    if not correo_request.placa or not correo_request.correo_destino:
        raise HTTPException(status_code=400, detail="Faltan parámetros necesarios")
    # metodo del servicio para enviar el correo
    await post_correo(correo_request)
    
    return {"mensaje": "Correo enviado exitosamente"}