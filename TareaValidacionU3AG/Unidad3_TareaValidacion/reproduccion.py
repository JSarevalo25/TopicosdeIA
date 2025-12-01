import random
class Reproduccion:
    def __init__(self):
        pass
    # Genera un hijo combinando dos rutas (progenitores)
    # Selecciona un segmento aleatorio del primer progenitor y lo copia al hijo.
    # Luego, completa el hijo con los municipios del segundo progenitor, respetando el orden
    # y evitando duplicados, para asegurar que la ruta resultante sea válida.
    def reproduccion(self, progenitor1, progenitor2):
        hijo = len(progenitor1) * [None]
        generacionX = int(random.random() * len(progenitor1))
        generacionY = int(random.random() * len(progenitor2))
        
        generacionInicial = min( generacionX,  generacionY)
        generacionFinal = max( generacionX, generacionY)

        hijo[generacionInicial:generacionFinal] = progenitor1[generacionInicial:generacionFinal]
        pos = generacionFinal
        for ciudad in progenitor2:
            if ciudad not in hijo:
                if pos >= len(hijo):
                    pos = 0
                hijo[pos] = ciudad
                pos += 1
        return hijo

    # Genera una nueva población de rutas a partir de un grupo de apareamiento.
    # Los primeros 'indivSelecionados' individuos se copian directamente.
    # El resto de la población se genera cruzando pares de individuos seleccionados aleatoriamente.
    def reproduccionPoblacion(self, grupoApareamiento, indivSelecionados):
        hijos = []
        tamano = len(grupoApareamiento) - indivSelecionados
        espacio = random.sample(grupoApareamiento, len(grupoApareamiento))

        for i in range(0,indivSelecionados):
            hijos.append(grupoApareamiento[i])
        
        for i in range(0, tamano):
            hijo = self.reproduccion(espacio[i], espacio[len(grupoApareamiento)-i-1])
            hijos.append(hijo)
        return hijos