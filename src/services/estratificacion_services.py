import pandas as pd
from src.repositories.estratificacion_reposiory import EstratificacionRepository
from src.services.parametro_service import ParametroService


class EstratificacionService:
    def __init__(self, conexion, sistem):
        self.reposicion = EstratificacionRepository(conexion)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem

    def estratificacion(self, tipo: str, anio: int):
        val_min = 0.01
        mal_max = 9999999999999.99
        if not tipo:
            raise ValueError("El tipo de empresa no puede estar vacío.")
        elif tipo == '0':
            val_min = 0.1
            mal_max = 1000000
        elif tipo == '1':
            val_min = 1000000.01
            mal_max = 10000000
        elif tipo == '2':
            val_min = 10000000.01
            mal_max = 50000000
        elif tipo == '3':
            val_min = 50000000.01
            mal_max = 9999999999999.99
        elif tipo == '%':
            val_min = 0.01
            mal_max = 9999999999999.99

        data = self.reposicion.estratificacion(
            val_minimo=val_min, val_maximo=mal_max, periodo=anio)
        if not data:
            raise ValueError(
                "No se encontraron datos de declaraciones a establecimeintos (respuesta vacía).")
        try:
            df = pd.DataFrame(data)
        except Exception as e:
            raise ValueError(f"No se pudo convertir a DataFrame: {e}")
        if df.empty:
            raise ValueError(
                "No se encontraron datos de declaraciones a establecimeintos  (DataFrame vacío).")
        return df
