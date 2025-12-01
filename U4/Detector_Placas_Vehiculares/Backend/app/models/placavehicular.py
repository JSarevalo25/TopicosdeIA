from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String, Integer
from app.db.database import Base

# Modelo de la tabla placas_vehicular en la base de datos

class PlacaVehicular(Base):
    __tablename__ = "placas_vehicular"

    placa_id = Column(String, primary_key=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    anio = Column(Integer, nullable=False)
    matricula_id = Column(String, ForeignKey("alumnos.matricula_id"), nullable=True)
    alumno = relationship("Alumno", back_populates="placas")