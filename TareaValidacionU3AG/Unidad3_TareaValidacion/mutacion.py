import random
class Mutacion:
    def __init__(self):
        pass
    
    # Aplica la operación de mutación a un individuo (ruta).
    # Recorre cada posición del individuo y, con una probabilidad igual a razonMutacion,
    # intercambia el municipio actual con otro municipio aleatorio de la ruta.
    def mutacion(self, individuo, razonMutacion):
        for swapped in range(len(individuo)):
            if(random.random() < razonMutacion):
                swapWith = int(random.random() * len(individuo))       
                lugar1 = individuo[swapped]
                lugar2 = individuo[swapWith]       
                individuo[swapped] = lugar2
                individuo[swapWith] = lugar1
        return individuo

    # Aplica la mutación a toda la población.
    # Itera sobre cada individuo de la población y le aplica la función de mutación,
    # generando una nueva población mutada.
    def mutacionPoblacion(self, poblacion, razonMutacion):
        pobMutada = []
        for ind in range(0, len(poblacion)):
            individuoMutar = self.mutacion(poblacion[ind], razonMutacion)
            pobMutada.append(individuoMutar)
        return pobMutada