import pandas as pd
from src.repositories.estratificacion_reposiory import EstratificacionRepository
from src.repositories.rpt_establecimientos_repository import RptEstablecimientoRepository
from src.services.parametro_service import ParametroService


class EstablecimientosService:
    def __init__(self, conexion, sistem):
        self.repositori = EstratificacionRepository(conexion)
        self.repositori_rpt = RptEstablecimientoRepository(conexion)
        self.sys = sistem


    def get_rpt_mora_x_actividad(self, cta_actividad:str="%"):
        if not self.sys["TpoCuenta"]:
            cuentas = ["111112%","111113%","111114%","11212203%","11212204%","11212205%","11212601","11212101","11111921%","112127%","1120120"]
        else:
            cuentas = ["117101%","117102%","117103%","11719801%","11719802%","11719803%","117197%","117196%","125990230%","112127%","1259903%"]
        cuentas.append(cta_actividad)
        data_res = self.repositori_rpt.obtener_mora_establecimiento_por_tipo(cta_cuentas_list=cuentas)
        if not data_res:
            raise ValueError(
                "No se Encontro Mora de Servicios (respuesta vacía).")
        try:
            df = pd.DataFrame(data_res)
        except Exception as e:
            raise ValueError(
                f"No se pudo convertir a DataFrame: (Mora Abonados por Servicio) {e}")
        if df.empty:
            raise ValueError(
                "No se Encontraro Mora de Abonados por Servicio  (DataFrame vacío).")
        return df

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

        data = self.repositori.estratificacion(
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
