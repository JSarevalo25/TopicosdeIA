from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from app.db.database import Base

# Modelo de la tabla alumnos en la base de datos

class Alumno(Base):
    __tablename__ = "alumnos"

    matricula_id = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    ape_paterno = Column(String, nullable=False)
    ape_materno = Column(String, nullable=False)
    correo = Column(String, nullable=False)
    celular = Column(String, nullable=False)
    carrera = Column(String, nullable=False)
    num_incidencias = Column(Integer, nullable=False, default="0")
    placas = relationship("PlacaVehicular", back_populates="alumno")