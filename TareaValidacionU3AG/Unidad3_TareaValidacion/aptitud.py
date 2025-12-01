class Aptitud:
    def __init__(self, ruta):
        self.ruta = ruta
        self.distancia = 0
        self.f_aptitud= 0.0
        
    # Calcula la distancia total de la ruta.
    # Recorre todos los municipios de la ruta y suma la distancia entre cada municipio,
    # incluyendo el regreso al punto inicial al final (ciclo cerrado).
    # Guarda el resultado en self.distancia.
    def distanciaRuta(self):
        if self.distancia == 0:
            distanciaRelativa = 0
            for i in range(0, len(self.ruta)):
                puntoInicial = self.ruta[i]
                if i + 1 < len(self.ruta):
                    puntoFinal = self.ruta[i + 1]
                else:
                    puntoFinal = self.ruta[0]
                distanciaRelativa += puntoInicial.distancia(puntoFinal)
            self.distancia = distanciaRelativa
        return self.distancia

    #  Calcula la aptitud de la ruta.
    #  Utiliza la función distanciaRuta para obtener la distancia recorrida y calcula la aptitud
    #  como 1/distancia para obtener la aptitud

    def rutaApta(self):
        distancia = self.distanciaRuta()
        self.f_aptitud = 1 / float(distancia)
        return self.f_aptitud