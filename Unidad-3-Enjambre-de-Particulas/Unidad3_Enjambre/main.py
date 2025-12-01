from datos import Datos
from optimizador_sensores import OptimizadorSensores
from visualizar import Visualizar

if __name__ == "__main__":
    # Se crea el objeto Datos y se cargan los datos del csv de cultivos
    datocsv = Datos("./Datos/cultivos.csv")
    data = datocsv.get_datos()

    # Creamos el objeto optimizador_sensores que preparara las variables para
    # encontrar la mejor distribución de sensores
    optimizador = OptimizadorSensores(data, n_sensores=5)
    mejor_costo, mejor_posicion = optimizador.optimizar(iters=30)
    mejores_posiciones = optimizador.get_mejores_posiciones()

    # Muestra de Resultados obtenidos
    print("--------------------------------------------------------")
    print(f"Mejor Costo: {mejor_costo:.2f}")
    print("Mejores posiciones para sensores (Latitud, Longitud):")
    for i, (lat, lon) in enumerate(mejores_posiciones, start=1):
        print(f"Sensor {i}: Latitud={lat:.6f}, Longitud={lon:.6f}")

    # Grafica de los sensores y cultivos
    visualizar = Visualizar()
    visualizar.mostrar(data, mejores_posiciones)
