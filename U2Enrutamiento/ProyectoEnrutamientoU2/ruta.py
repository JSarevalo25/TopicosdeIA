import random as rd
import numpy as np

class Ruta:
    # Constructor que recibe el objeto datos
    def __init__(self, datos):
        self.datos = datos
    # evaluar el costo de una ruta
    def evaluar(self, ruta):
        costo = 0
        for i in range(len(ruta)-1):
            origen = ruta[i]
            destino = ruta[i+1]
            costo += self.datos.matriz_costo[origen-1, destino-1]
        return costo
    # generar un vecino intercambiando dos tiendas en la ruta
    def generar_vecino(self, ruta):
        vecino = ruta.copy()
        if len(vecino) <= 2:
            return vecino
        i, j = rd.sample(range(1, len(vecino)-1), 2)
        vecino[i], vecino[j] = vecino[j], vecino[i]
        return vecino
    # Funcion de probabilidad para el criterio de aceptacion
    def probabilidad(self, delta, temp):
        return np.exp(-delta / temp)