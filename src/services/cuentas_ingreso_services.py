from src.repositories.cuenta_ingreso_repository import CuentaIngresoRepository


class CuentasService:
    def __init__(self, conexion):
        self.repository = CuentaIngresoRepository(conexion)

    def get_cuentas_abonado(self):
        data_res = self.repository.obtener_lista_cuentas_tipo_impuesto(tipo=3)
        if not data_res:
            raise ValueError(
                "No se Encontraron Cuentas de Ingreso para Abonados de Servicios (respuesta vacía).")
        return data_res

    def get_cuentas_actividad_aconomica(self):
        data_res = self.repository.obtener_lista_cuentas_tipo_impuesto(tipo=0)
        if not data_res:
            raise ValueError(
                "No se Encontraron Cuentas de Ingreso para actividades economicas de ICS (respuesta vacía).")
        return data_res
