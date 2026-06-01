import pandas as pd
from src.repositories.reportes_ingresos_depto_mensual_repository import IngresosDeptosMensualRepository
from src.services.parametro_service import ParametroService


class RptIngresosDeptosMensualService:
    def __init__(self, conexion, sistem):
        self.repo_ingresos = IngresosDeptosMensualRepository(conexion)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem

    def ingresos_mensual_catastro(self,  anio):
        data_res = self.repo_ingresos.obtener_mensual_catastro(anio=anio)

        if not data_res:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados Catastro (respuesta vacía).")
        try:
            df = pd.DataFrame(data_res)
        except Exception as e:
            raise ValueError(
                f"No se pudo convertir a DataFrame: (Ingresos Diarios Catastro) {e}")
        if df.empty:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados Catastro  (DataFrame vacío).")
        return df

    def ingresos_mensual_tributaria_otras_tasas(self,  anio):
        data_res = self.repo_ingresos.obtener_mensual_ics_otras(anio=anio)

        if not data_res:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados Pago de Otras Tasas (respuesta vacía).")
        try:
            df = pd.DataFrame(data_res)
        except Exception as e:
            raise ValueError(
                f"No se pudo convertir a DataFrame: (Ingresos Diarios Pago de Otras Tasas) {e}")
        if df.empty:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados Pago de Otras Tasas  (DataFrame vacío).")
        return df

    def ingresos_mensual_tributaria_inmuebles(self,  anio):
        data_res = self.repo_ingresos.obtener_mensual_ics_bienes(anio=anio)

        if not data_res:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados Pago de Bienes Inmuebles (respuesta vacía).")
        try:
            df = pd.DataFrame(data_res)
        except Exception as e:
            raise ValueError(
                f"No se pudo convertir a DataFrame: (Ingresos Diarios Pago de Bienes Inmuebles) {e}")
        if df.empty:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados Pago de Bienes Inmuebles  (DataFrame vacío).")
        return df

    def ingresos_mensual_tributaria_comercio(self, anio):
        data_res = self.repo_ingresos.obtener_mensual_ics_comercio(anio=anio)

        if not data_res:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados Pago de Industria y Comercio (respuesta vacía).")
        try:
            df = pd.DataFrame(data_res)
        except Exception as e:
            raise ValueError(
                f"No se pudo convertir a DataFrame: (Ingresos Diarios Pago de Industria y Comercio) {e}")
        if df.empty:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados Pago de Industria y Comercio  (DataFrame vacío).")
        return df

    def ingresos_mensual_tributaria_personal(self, anio):
        data_res = self.repo_ingresos.obtener_mensual_ics_personal(anio=anio)

        if not data_res:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados Pago de Impuesto Personal (respuesta vacía).")
        try:
            df = pd.DataFrame(data_res)
        except Exception as e:
            raise ValueError(
                f"No se pudo convertir a DataFrame: (Ingresos Diarios Pago de Impuesto Personal) {e}")
        if df.empty:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados Pago de Impuesto Personal  (DataFrame vacío).")
        return df

    def ingresos_mensual_uma(self,  anio):
        data_res = self.repo_ingresos.obtener_mensual_uma(anio=anio)

        if not data_res:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados UMA (respuesta vacía).")
        try:
            df = pd.DataFrame(data_res)
        except Exception as e:
            raise ValueError(
                f"No se pudo convertir a DataFrame: (Ingresos Diarios UMA) {e}")
        if df.empty:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados UMA  (DataFrame vacío).")
        return df

    def ingresos_mensual_justicia(self,  anio):
        data_res = self.repo_ingresos.obtener_mensual_justicia(anio=anio)

        if not data_res:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados Direccion de Justicia Municipal (respuesta vacía).")
        try:
            df = pd.DataFrame(data_res)
        except Exception as e:
            raise ValueError(
                f"No se pudo convertir a DataFrame: (Ingresos Diarios Direccion de Justicia Municipal) {e}")
        if df.empty:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados Direccion de Justicia Municipal  (DataFrame vacío).")
        return df

    def ingresos_mensual_secretaria(self,  anio):
        data_res = self.repo_ingresos.obtener_mensual_secretaria(anio=anio)

        if not data_res:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados Departamento Secretaria Municipal (respuesta vacía).")
        try:
            df = pd.DataFrame(data_res)
        except Exception as e:
            raise ValueError(
                f"No se pudo convertir a DataFrame: (Ingresos Diarios Departamento Secretaria Municipal) {e}")
        if df.empty:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados Departamento Secretaria Municipal  (DataFrame vacío).")
        return df

    def ingresos_mensual_procamut(self,  anio):
        data_res = self.repo_ingresos.obtener_mensual_procamut(anio=anio)

        if not data_res:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados PROCAMUT (respuesta vacía).")
        try:
            df = pd.DataFrame(data_res)
        except Exception as e:
            raise ValueError(
                f"No se pudo convertir a DataFrame: (Ingresos Diarios PROCAMUT) {e}")
        if df.empty:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados PROCAMUT  (DataFrame vacío).")
        return df

    def ingresos_mensual_desarrollo_urbano(self,  anio):
        data_res = self.repo_ingresos.obtener_mensual_urbanizacion(anio=anio)

        if not data_res:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados Unidad de Desarrollo Urbano (respuesta vacía).")
        try:
            df = pd.DataFrame(data_res)
        except Exception as e:
            raise ValueError(
                f"No se pudo convertir a DataFrame: (Ingresos Diarios Unidad de Desarrollo Urbano) {e}")
        if df.empty:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Unidad de Desarrollo Urbano  (DataFrame vacío).")
        return df
