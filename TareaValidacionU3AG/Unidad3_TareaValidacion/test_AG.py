from municipio import Municipio
from aptitud import Aptitud
from ruta import Ruta
from reproduccion import Reproduccion
from mutacion import Mutacion

# Creacion de una ruta conocida par aprobar la Aptitud
# Ruta: A -> B -> C -> D 
#Se crea una ruta conocida que forma un cuadrado de lado 1.
#La distancia total esperada es 4.0 y la aptitud esperada es 0.25.
#Esta prueba valida que la función de aptitud calcula correctamente la distancia y la aptitud de la ruta.

munis = [
    Municipio('A', 0, 0),
    Municipio('B', 0, 1),
    Municipio('C', 1, 1),
    Municipio('D', 1, 0)
]
apt = Aptitud(munis)
print("Distancia esperada: 4.0, calculada:", apt.distanciaRuta())
print("Aptitud esperada: 0.25, calculada:", apt.rutaApta())

# Prueba de selección
# Se crea una población inicial con cuatro rutas distintas:
# - munis: ruta original (A -> B -> C -> D)
# - munis[::-1]: ruta invertida (D -> C -> B -> A)
# - munis[1:] + munis[:1]: ruta comenzando en B (B -> C -> D -> A)
# - munis[2:] + munis[:2]: ruta comenzando en C (C -> D -> A -> B)
# Se verifica que el método seleccionRutas elige rutas (individuos) de la población
# priorizando aquellas con mejor aptitud. Al imprimir los índices seleccionados,
# se puede observar que los individuos con mayor aptitud son seleccionados más frecuentemente.
# Lo que indica que el proceso de seleccion funciona correctamente.
poblacion = [munis, munis[::-1], munis[1:] + munis[:1], munis[2:] + munis[:2]]
popRanked = Ruta.clasificacionRutas(poblacion)
seleccionados = Ruta.seleccionRutas(popRanked, 2)
print("Índices seleccionados:", seleccionados)

# Prueba de cruce
# Se verifica que el método de cruce genera un hijo combinando dos rutas (padres) válidas.
# El hijo resultante debe contener todos los municipios sin repetir y en una nueva combinación,
# asegurando que la descendencia sea válida.

rp = Reproduccion()
padre1 = munis
padre2 = munis[::-1]
hijo = rp.reproduccion(padre1, padre2)
print("Hijo generado:", hijo)
#Ordena ambas listas por coordenadas (x,y) para comparar 
#si el hijo contiene los mismos municipios que los padres
print("¿Es válido?", sorted(hijo, key=lambda m: (m.x, m.y)) == sorted(munis, key=lambda m: (m.x, m.y)))

# Prueba de mutación
# Se verifica que el método de mutación modifica el orden de los municipios en la ruta,
# pero mantiene todos los municipios originales sin repetir ni omitir ninguno.
mu = Mutacion()
individuo = munis[:]
mutado = mu.mutacion(individuo, 0.1)
print("Individuo original:", [m.nombre for m in munis])
print("Individuo mutado:", [m.nombre for m in mutado])
#Valida si el individuo mutado contiene los mismos municipios que el original
print("¿Es válido?", sorted(mutado, key=lambda m: (m.x, m.y)) == sorted(munis, key=lambda m: (m.x, m.y)))
