import random as rd

# Pasamos parametros iniciales del algoritmo recocido
class AlgoritmoRecocido:
    def __init__(self, ruta, temp_inicial=1000, alpha=0.95, iter_por_temp=100, temp_final=0.01):
        self.ruta = ruta
        self.temp_inicial = temp_inicial
        self.alpha = alpha
        self.iter_por_temp = iter_por_temp
        self.temp_final = temp_final
    # Funcion de Algoritmo Recocido
    def ejecutar_algoritmo(self, cd, tiendas):
        temp = self.temp_inicial
        solucion_actual = [cd] + tiendas + [cd] # Creamos la solucion inicial
        costo_actual = 0 
        while temp >= self.temp_final: 
            for _ in range(self.iter_por_temp):
                ruta_vecino = self.ruta.generar_vecino(solucion_actual) 
                costo_vecino = self.ruta.evaluar(ruta_vecino) 
                delta = costo_vecino - costo_actual # Obtenemos Delta
                if delta < 0 or rd.uniform(0,1) < self.ruta.probabilidad(delta, temp): # Validar el criterio de aceptacion
                    solucion_actual = ruta_vecino 
                    costo_actual = costo_vecino
            temp *= self.alpha # Reducimos la temperatura
        return solucion_actual, costo_actual 