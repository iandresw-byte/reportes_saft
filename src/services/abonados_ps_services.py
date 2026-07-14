import pandas as pd

from src.repositories.rpt_abonados_sp_repository import AbonadosRepository


class AbonadosSPService:
    def __init__(self, conexion):
        self.repository = AbonadosRepository(conexion)

    def get_abonado_x_servicio(self, cuentas):
  
        data_res = self.repository.obtener_mora_por_abonado_servicio(cuentas["CtaIngreso"],cuentas["CtaRecuperacion"],cuentas["CtaInteres"],cuentas["CtaRecargos"])
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
    

