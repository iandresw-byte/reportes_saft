import pandas as pd
from src.repositories.sar_reporte_repository import SARReportesRepository
from src.services.parametro_service import ParametroService


class SARReportesService:
    def __init__(self, conexion, sistem):
        self.reposicion = SARReportesRepository(conexion)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem

    def declaraciones_sar(self, val_min: float, anio: int):

        data = self.reposicion.declaraciones_sar(
            val_minimo=val_min,  periodo=anio)
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
