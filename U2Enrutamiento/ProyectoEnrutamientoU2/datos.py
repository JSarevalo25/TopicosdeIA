import pandas as pd
import numpy as np

class Datos:
    # En el constructor se leen los archivos excel y se crean las matrices numpy necesarias
    def __init__(self, archivo_distancias, archivo_costos_combustible, archivo_tiendas):
        self.distancias_df = pd.read_excel(archivo_distancias)
        self.costos_df = pd.read_excel(archivo_costos_combustible)
        self.centrostiendas_df = pd.read_excel(archivo_tiendas)
        
        self.matriz_distancias = self.distancias_df.values
        self.matriz_costos_combustible = self.costos_df.values
        self.matriz_costo = self.matriz_distancias * self.matriz_costos_combustible
        # Diccionario que mapea cada centro de distribucion con sus tiendas
        self.cd_tiendas = self._procesar_cd_tiendas()

    def _procesar_cd_tiendas(self):
        cd_tiendas = {}
        for col in self.centrostiendas_df.columns: 
            tiendas = self.centrostiendas_df[col].dropna().astype(int).tolist() 
            cd_index = int(col.replace("C", "")) # Extraemos el numero del centro de distribucion
            cd_tiendas[cd_index] = tiendas # insertamos en el diccionario
        return cd_tiendas