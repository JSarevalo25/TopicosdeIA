# Integrantes
# Sanchez Arevalo Jose Antonio
# Felix Avendaño Mateo
from agModificado import AlgoritmoGenetico 
from municipio import Municipio
if __name__ == "__main__":
    # Se define una lista de ciudades (municipios) con sus coordenadas.
    ciudades = [
        Municipio("Madrid", 40.4168, -3.7038),
        Municipio("Barcelona", 41.3784, 2.1925),
        Municipio("Valencia", 39.4699, -0.3763),
        Municipio("Sevilla", 37.3886, -5.9953),
        Municipio("Bilbao", 43.2630, -2.9350),
        Municipio("Zaragoza", 41.6488, -0.8891),
        Municipio("Malaga", 36.7213, -4.4214),
        Municipio("Murcia", 37.9847, -1.1287),
        Municipio("Palma", 39.5696, 2.6502),
        Municipio("Las Palmas", 28.1235, -15.4363)
    ]
    # creamos el objeto AlgoritmoGenetico y iniciamos la funcion ejecutar para
    # correr el algoritmo genetico con las configuraciones deseadas.
    ag = AlgoritmoGenetico()
    mejorruta=ag.ejecutar(poblacion=ciudades, 
        tamanoPoblacion=100, 
        indivSelecionados=20,
        razonMutacion=0.01, 
        generaciones=500)
    
    # Imprime la mejor ruta encontrada.
    print("Mejor Ruta Encontrada:")
    for municipio in mejorruta:
        print(municipio)

