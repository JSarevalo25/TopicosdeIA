# importando las librerias necesarias
import base64
from fastapi import HTTPException
from app.schemas.dtos.deteccion_placa_request import DeteccionPlacaRequest
from app.db.database import SessionLocal
from app.models.placavehicular import PlacaVehicular
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ultralytics import YOLO
from paddleocr import PaddleOCR
import cv2 
import re
import numpy as np
import os
# Prepara los modelos necesarios (UNA SOLA VEZ AL ARRANCAR EL SERVIDOR)
# inicializa el modelo YOLOv11
modelo = YOLO('./app/services/detectorModel/best.pt')
# inicializa el modelo OCR PaddleOCR 
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Esta funcion asincrona busca en la base de datos la placa vehicular y 
# retorna la informacion del carro y del dueño (estudiante)
async def buscar_por_placa(placa: str):
    async with SessionLocal() as session:
        stmt = select(PlacaVehicular).options(selectinload(PlacaVehicular.alumno)).where(PlacaVehicular.placa_id == placa)
        result = await session.execute(stmt)
        carro = result.scalars().first()
    return carro
    
# Esta funcion asincrona detecta la placa en la imagen enviado en base 64
# para posteriormente extrae el texto de la placa usando OCR y retornar el texto de la placa    
async def detectar_placa(imagen_base64: str):
    
    # Decodifica la imagen de base64 a bytes y luego a una imagen opencv
    try:
        imagen_bytes = base64.b64decode(imagen_base64)
        np_arr = np.frombuffer(imagen_bytes, np.uint8)
        imagen = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except:
        raise HTTPException(status_code=400, detail="Imagen inválida")

    # realiza la deteccion de la placa con YOLOv11
    resultados = modelo(imagen)
  
    # procesa los resultados de la deteccion
    for resultado in resultados:
 
        if resultado.boxes is None or len(resultado.boxes) == 0:
        # No se detectó ninguna placa en esta imagen
            continue  # pasa al siguiente resultado (si hay)
 
        index_placa = (resultado[0].boxes.cls == 1).nonzero(as_tuple = True)[0]
        
        for i in index_placa:
            # obtiene la confianza de la caja
            conf = resultado.boxes.conf[i].item()
            
            # si la confianza es mayor al 50%
            if conf >= 0.5:
                
                # obtener coordenadas de la caja
                xyxy = resultado.boxes.xyxy[i].squeeze().tolist()

                x1, y1 = int(xyxy[0]), int(xyxy[1])
                x2, y2 = int(xyxy[2]), int(xyxy[3])

                # recortar la imagen de la placa
                placa_img = imagen[y1:y2, x1:x2]

                # procesar la imagen de la placa para OCR
                
                resultado_ocr = ocr.predict(cv2.cvtColor(placa_img, cv2.COLOR_BGR2RGB))
                
                # ordenar los textos detectados para que salgan los textos detectados 
                # en orden de izquierda a derecha
                textos = resultado_ocr[0]['rec_texts']
                
                # extrae el texto de la placa usando expresiones regulares
                texto_extraido_placa = extraer_placa(textos)
                
                # retorna el texto de la placa si se extrajo correctamente
                if texto_extraido_placa:
                    return {"texto_placa": texto_extraido_placa}
                else:
                    raise HTTPException(status_code=422, detail="OCR no pudo leer la placa")

    # Si YOLO no detectó nada
    raise HTTPException(status_code=404, detail="No se detectó ninguna placa en la imagen")


# Esta funcion extrae el texto de la placa usando expresiones regulares
# porque las placas tienen formatos especificos y si por ejemplo
# detectara otros textos que no son placas, los descartaria
# es un filtrado adicional para mejorar el ocr
def extraer_placa(textos):
    patrones=[
        r"^[A-Z]{3}-\d{2}-\d{2}$",  # Formato ABC-12-23
        r"^[A-Z]{2}-\d{3}$",  # Formato AB-123
        r"^[A-Z]{2}-\d{2}-\d{3}$",  # Formato AB-12-345
    ]
    
    # recorre todos los textos detectados y busca coincidencias con los patrones
    # posteriormente retorna la placa sin guiones para luego buscarlo en la base de datos
    for texto in textos:
        texto = texto.upper()
        for patron in patrones:
            match = re.search(patron, texto.replace(" ", ""))
            if match:
                placa = match.group(0)
                placa_sin_guiones = placa.replace("-", "")
                return placa_sin_guiones
    return None