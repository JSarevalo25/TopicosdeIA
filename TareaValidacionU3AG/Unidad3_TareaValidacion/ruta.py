import random
import operator
import pandas as pd
import numpy as np
from aptitud import Aptitud as ap

class Ruta:
    def __init__(self):
        pass

    #  Genera una ruta aleatoria a partir de una lista de municipios.
    def crearRuta(listaMunicipios):
        route = random.sample(listaMunicipios, len(listaMunicipios))
        return route

    #  Calcula la aptitud de cada ruta en la población y las ordena de mejor a peor.
    def clasificacionRutas(poblacion):
        fitnessResults = {}
        for i in range(0,len(poblacion)):
            fitnessResults[i] = ap(poblacion[i]).rutaApta()
        return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

    # Selecciona los individuos que serán padres para la siguiente generación.
    def seleccionRutas(popRanked, indivSelecionados):
        resultadosSeleccion = []
        df = pd.DataFrame(np.array(popRanked), columns=["Indice","Aptitud"])
        df['cum_sum'] = df.Aptitud.cumsum()
        df['cum_perc'] = 100*df.cum_sum/df.Aptitud.sum()
        
        for i in range(0, indivSelecionados):
            resultadosSeleccion.append(popRanked[i][0])
        for i in range(0, len(popRanked) - indivSelecionados):
            seleccion = 100*random.random()
        for i in range(0, len(popRanked)):
            if seleccion <= df.iat[i,3]:
                resultadosSeleccion.append(popRanked[i][0])
                break
        return resultadosSeleccion
