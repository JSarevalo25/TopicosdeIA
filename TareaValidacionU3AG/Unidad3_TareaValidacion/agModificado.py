from ruta import Ruta as ru
from reproduccion import Reproduccion as rp
from mutacion import Mutacion as mu
class AlgoritmoGenetico:

  def __init__(self):
      self.ru = ru()
      self.mu = mu()
      self.rp = rp()
      pass
  
  # Genera la población inicial de rutas para el algoritmo genético.
  # Crea la cantidad de "tamanoPob" rutas aleatorias a partir de la lista de municipios proporcionada.
  # Cada ruta representa un individuo de la población inicial.
  def poblacionInicial(self, tamanoPob,listaMunicipios):
    poblacion = []
    for i in range(0, tamanoPob):
      poblacion.append(ru.crearRuta(listaMunicipios))
    return poblacion
  
  # Forma el grupo de apareamiento a partir de los individuos seleccionados.
  # Utiliza los índices de los individuos seleccionados para extraer las rutas correspondientes
  # de la población y formar el grupo que será usado para el cruce (reproducción).
  def grupoApareamiento(self, poblacion, resultadosSeleccion):
    grupoApareamiento = []
    for i in range(0, len(resultadosSeleccion)):
      index = resultadosSeleccion[i]
      grupoApareamiento.append(poblacion[index])
    return grupoApareamiento

  def nuevaGeneracion(self, generacionActual, indivSelecionados, razonMutacion):
    #clasificar rutas 
    popRanked = ru.clasificacionRutas(generacionActual)
    #seleccion de los candidatos
    selectionResults = ru.seleccionRutas(popRanked, indivSelecionados)
    #generar grupo de apareamiento
    grupoApa = self.grupoApareamiento(generacionActual, selectionResults)
    #generacion de la poblacion cruzada, reproducida
    hijos = self.rp.reproduccionPoblacion(grupoApa, indivSelecionados)
    #incluir las mutaciones en la nueva generación 
    nuevaGeneracion = self.mu.mutacionPoblacion(hijos, razonMutacion)
    return nuevaGeneracion


  # Ejecuta el algoritmo genetico
  # Inicializa la población, muestra la distancia inicial de la mejor ruta,
  # y luego evoluciona la población durante el número de generaciones especificado,
  # aplicando selección, cruce y mutación en cada ciclo.
  # Al finalizar, muestra la distancia final de la mejor ruta encontrada y la retorna.

  def ejecutar(self, poblacion, tamanoPoblacion, indivSelecionados, razonMutacion, generaciones):
    pop = self.poblacionInicial(tamanoPoblacion, poblacion)
    print("Distancia Inicial: " + str(1 / ru.clasificacionRutas(pop)[0][1]))
    for _ in range(0, generaciones):
      pop = self.nuevaGeneracion(pop, indivSelecionados, razonMutacion)
    print("Distancia Final: " + str(1 / ru.clasificacionRutas(pop)[0][1]))
    bestRouteIndex = ru.clasificacionRutas (pop)[0][0]
    mejorRuta = pop[bestRouteIndex]
    return mejorRuta



