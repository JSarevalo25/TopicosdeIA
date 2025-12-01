# Importamos las librerias necesarias
import base64
from email import encoders
from email.mime.base import MIMEBase
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl 
from app.schemas.dtos.correo_request import CorreoRequest
from app.db.database import SessionLocal
from app.models.alumnos import Alumno
from app.models.placavehicular import PlacaVehicular
from sqlalchemy import select
from sqlalchemy.orm import selectinload



# Definir las credenciales del correo remitente
# IMPORTANTE: SOLO DEBE DE USAR UNA CUENTA DE GMAIL CREADA PARA ESTE PROPOSITO
# YA QUE SE EXPONEN LAS CREDENCIALES AQUI

# Si usted tiene la cuenta verificada a 2 pasos, debe de crear una contraseña de aplicacion
# si no entonces puede usar su contraseña normal de gmail
# Solo debe de modificar las lineas del remitente, password y destinatario_institucional

#---------------------------------------------------------
remitente = ""#<-- Poner aqui el correo del remitente
password = "" #<-- poner aqui la contraseña o contraseña de aplicacion (si tiene verificacion en 2 pasos))
destinatario_institucional = "" #<-- poner aqui el correo institucional que recibira los reportes
#---------------------------------------------------------

# Este metodo lo que hace es buscar el alumno asociado a la placa
# posteriormente incrementa en 1 el numero de incidencias
async def incrementar_incidencia(placa: str) -> int:
       async with SessionLocal() as session:
        # Buscar la placa y el alumno asociado
        stmt = select(PlacaVehicular).where(PlacaVehicular.placa_id == placa).options(selectinload(PlacaVehicular.alumno))
        result = await session.execute(stmt)
        placa_obj = result.scalars().first()
        if not placa_obj:
            return 0  

        alumno_obj = placa_obj.alumno
        if not alumno_obj:
            return 0  

        # Incrementa el número de incidencias
        # y actualiza en la base de datos
        alumno_obj.num_incidencias += 1
        await session.commit()
        return alumno_obj.num_incidencias
    
# Este método envia un correo con el cuerpo, asunto y la imagen
async def enviar_correo_adjunto(destinatario, asunto, cuerpo, image_bytes):
    
    # crea el mensaje del correo
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    
    # Pone el cuerpo del correo
    msg.attach(MIMEText(cuerpo, 'plain'))
    
    # Adjunta la imagen
    part = MIMEBase("application", "octet-stream")
    part.set_payload(image_bytes)
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= placa.jpg",
    )
    msg.attach(part)
    
    # Configurar el servidor SMTP
    # usa el servidor smtp de gmail con conexion segura ssl
    # para despues logearse y enviar el correo
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context= context) as server:
        server.login(remitente, password)
        server.sendmail(msg["From"], destinatario, msg.as_string())


async def post_correo(correo_request: CorreoRequest):
    
    # Actualizara el numero de incidencias del estudiante en la BD incrementando 1
    nuevas_incidencias = await incrementar_incidencia(correo_request.placa)

    # Reemplazara el numero de incidencias en el objeto correo_request.num_incidencias
    correo_request.num_incidencias = nuevas_incidencias
    
    # Decodifica la imagen base64 a bytes
    image_bytes = base64.b64decode(correo_request.image_base64)
    
# Inicia preparando el primer correo para la institución    
# para poder prepara el correo necesita el asunto y el cuerpo 
    asunto = "Vehiculo mal estacionado detectado en el campus"
    cuerpo = mensajecorreoInstitucion(correo_request) # < -- Aqui genera el cuerpo del correo para la institucion
    # pasa a enviar el correo institucional con la imagen adjunta
    await enviar_correo_adjunto(destinatario_institucional, asunto, cuerpo, image_bytes)    
# Inicia Preparando el segundo correo para el estudiante 
    asunto = "Se ha detectado un vehiculo mal estacionado asociado a su matrícula"
    cuerpo = mensajecorreoEstudiante(correo_request) # < -- Aqui genera el cuerpo del correo para el estudiante
    # pasa a enviar el correo del estudiante con la imagen adjunta
    await enviar_correo_adjunto(correo_request.correo_destino, asunto, cuerpo, image_bytes)


# Genera el cuerpo del correo para el estudiante con ayuda de los datos recibidos
# dependiendo del numero de incidencias genera un mensaje diferente
def mensajecorreoEstudiante(correo_request: CorreoRequest):
    
    if correo_request.num_incidencias >= 3:
        return f"""
    Se ha detectado que su vehículo se encuentra mal estacionado en el campus.

    Esta es su {correo_request.num_incidencias} incidencia, por lo que:

    Se aplicará una sanción temporal: 
    Su vehículo NO podrá ingresar a la institución durante los próximos 3 días.
        
    Placa del vehiculo: 
    
    -{correo_request.placa}
    
    Marca, modelo y año del vehiculo:
    
    -{correo_request.marca_modelo_año}
    
    Nombre completo del estudiante asociado al vehiculo:
    
    -{correo_request.nombre_estudiante + " " + correo_request.apellidos_estudiante}
    
    Carrera:
     
    -{correo_request.carrera_estudiante}
    
    Numero de incidencias del estudiante:
    
    -{str(correo_request.num_incidencias)}
    
    Se adjunta la fotografia de la placa capturada. y coordenadas GPS.
    
    Coordenadas GPS: 
    
    -Latitud: {correo_request.latitud}, Longitud: {correo_request.longitud}

    Cualquier queja o apelación debe ser dirigida al departamento correspondiente.
    """
    else:
        return f"""
    
    Se ha detectado su vehiculo mál estacionado en el campus.
    
    Placa del vehiculo: 
    
    -{correo_request.placa}
    
    Marca, modelo y año del vehiculo:
    
    -{correo_request.marca_modelo_año}
    
    Nombre completo del estudiante asociado al vehiculo:
    
    -{correo_request.nombre_estudiante + " " + correo_request.apellidos_estudiante}
    
    Carrera:
     
    -{correo_request.carrera_estudiante}
    
    Numero de incidencias del estudiante:
    
    -{str(correo_request.num_incidencias)}
    
    Se adjunta la fotografia de la placa capturada. y coordenadas GPS.
    
    Coordenadas GPS: 
    
    -Latitud: {correo_request.latitud}, Longitud: {correo_request.longitud}

    Recuerde estacionar su vehiculo en las áreas correspondientes y estacionarse de manera correcta para evitar futuras incidencias.
    
    Tomar en cuenta que 3 incidencias puede resultar en la prohibicion de ingreso vehicular.
    
    """

# Genera el cuerpo del correo para la institucion con ayuda de los datos recibidos
# dependiendo del numero de incidencias genera un mensaje diferente
def mensajecorreoInstitucion(correo_request: CorreoRequest):
    if correo_request.num_incidencias >= 3:
        return f"""
        Se ha detectado un vehículo mal estacionado en el campus.

        El estudiante asociado ha alcanzado {correo_request.num_incidencias} incidencias, 
        por lo que debe aplicarse la sanción correspondiente de restricción de ingreso vehicular.
        
        Placa del vehiculo: 

        -{correo_request.placa}

        Marca y Modelo y año del vehiculo:

        -{correo_request.marca_modelo_año}

        Nombre completo del Estudiante asociado al vehiculo:

        -{correo_request.nombre_estudiante + " " + correo_request.apellidos_estudiante}

        Numero de incidencias del estudiante:

        -{str(correo_request.num_incidencias)}

        Carrera:

        -{correo_request.carrera_estudiante}

        Correo del estudiante asociado:

        -{correo_request.correo_destino}

        Se adjunta la fotografia de la placa capturada. y coordenadas GPS.

        Coordenadas GPS: 

        -Latitud: {correo_request.latitud}, Longitud: {correo_request.longitud}

    """

    else:
        return f"""
        Se ha detectado un vehiculo mál estacionado en el campus.
        
        Placa del vehiculo: 
        
        -{correo_request.placa}
        
        Marca y Modelo y año del vehiculo:
        
        -{correo_request.marca_modelo_año}
        
        Nombre completo del Estudiante asociado al vehiculo:
        
        -{correo_request.nombre_estudiante + " " + correo_request.apellidos_estudiante}
        
        Numero de incidencias del estudiante:
        
        -{str(correo_request.num_incidencias)}
        
        Carrera:
        
        -{correo_request.carrera_estudiante}
        
        Correo del estudiante asociado:
        
        -{correo_request.correo_destino}
        
        Se adjunta la fotografia de la placa capturada. y coordenadas GPS.
        
        Coordenadas GPS: 
        
        -Latitud: {correo_request.latitud}, Longitud: {correo_request.longitud}
        
        """