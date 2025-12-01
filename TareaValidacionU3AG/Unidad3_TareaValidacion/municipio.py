import numpy as np

class Municipio:
    def __init__(self, nombre, x, y):
        self.nombre = nombre
        self.x = x
        self.y = y

    # cálculo de la distancia relativa mediante Teo.Pitágoras
    def distancia(self, municipio):
        xDis = abs(self.x - municipio.x)
        yDis = abs(self.y - municipio.y)
        distancia = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distancia

    # devuelve un listado con las coordenadas y el nombre
    def __repr__(self):
        return f"{self.nombre} ({self.x},{self.y})"
