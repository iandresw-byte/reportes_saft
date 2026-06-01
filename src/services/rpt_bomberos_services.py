from datetime import date
import pandas as pd
from src.repositories.bomberos_repository import BomberosRepository
from src.services.parametro_service import ParametroService


class RptBomberosService:
    def __init__(self, conexion, sistem):
        self.repositorio = BomberosRepository(conexion)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem

    def obtener_pagos_bomberos(self, fecha_ini: date, fecha_fin: date, tipo_cta):
        if not tipo_cta:
            data = self.repositorio.obtener_pagos_bomberos_detallado_gobernacion(
                fecha_ini, fecha_fin)
        else:
            data = self.repositorio.obtener_pagos_bomberos_detallado_sami(
                fecha_ini, fecha_fin)
        if not data:
            raise ValueError(
                "No se encontraron datos de pago de bomberos detallado (respuesta vacía).")
        try:
            df = pd.DataFrame(data)
        except Exception as e:
            raise ValueError(
                f"No se pudo convertir a DataFrame: pago de bomberos detallado  {e}")
        if df.empty:
            raise ValueError(
                "No se encontraron datos de pago de bomberos detallado  (DataFrame vacío).")
        return df

    def obtener_pagos_bomberos_cuenta(self, fecha_ini: date, fecha_fin: date):

        data = self.repositorio.obtener_pagos_bomberos_cuenta_sami(
            fecha_ini, fecha_fin)
        if not data:
            raise ValueError(
                "No se encontraron datos de pago de bomberos detallado (respuesta vacía).")
        try:
            df = pd.DataFrame(data)
        except Exception as e:
            raise ValueError(
                f"No se pudo convertir a DataFrame: pago de bomberos detallado  {e}")
        if df.empty:
            raise ValueError(
                "No se encontraron datos de pago de bomberos detallado  (DataFrame vacío).")
        return df
