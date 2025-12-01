### Integrantes:
# - Felix Avendaño Mateo
# - Sánchez Arévalo José Antonio
###

### Importar las clases 
from datos import Datos
from ruta import Ruta
from algoritmo_recocido import AlgoritmoRecocido

# Crear los objetos de las clases
# 1.-Datos(Pasando las ubicaciones de los archivos excel)
datos = Datos(
    "./DatosExcel/matriz_distancias.xlsx",
    "./DatosExcel/matriz_costos_combustible.xlsx",
    "./DatosExcel/centrostiendas.xlsx"
)
# 2.-Ruta(Pasando el objeto datos)
ruta_obj = Ruta(datos)

# 3.-AlgoritmoRecocido(Pasando el objeto ruta)
recocido = AlgoritmoRecocido(ruta_obj)

# Realizar la prueba de algoritmo recocido con un centro de distribucion
# En este caso Centro de distribucion 1
cd = 1
tiendas = datos.cd_tiendas[cd] # Sacamos las tiendas que estan en el centro de distribucion correspondiente
# Pasamos el centro de distribucion y las tiendas para obtener la mejor ruta y su costo
mejor_ruta, mejor_costo = recocido.ejecutar_algoritmo(cd, tiendas) 

# Mostrar resultados del centro de distribucion
print(f"Centro {cd}: Costo total = {mejor_costo:.3f}")
print(f"Ruta: {mejor_ruta}\n")
print("Detalles por tramo:")
for i in range(len(mejor_ruta)-1):
    origen = mejor_ruta[i]
    destino = mejor_ruta[i+1]
    distancia = datos.matriz_distancias[origen-1, destino-1]
    costo_comb = datos.matriz_costos_combustible[origen-1, destino-1]
    costo_total = datos.matriz_costo[origen-1, destino-1]
    print(f"De {origen} a {destino}: Distancia = {distancia:.3f}, Costo combustible = {costo_comb:.3f}, Costo total = {costo_total:.3f}")
