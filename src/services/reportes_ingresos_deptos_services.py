import pandas as pd
from src.repositories.reportes_ingresos_depto_repository import IngresosDeptosRepository
from src.services.parametro_service import ParametroService


class RptIngresosDeptosService:
    def __init__(self, conexion, sistem):
        self.repo_ingresos = IngresosDeptosRepository(conexion)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem

    def ingresos_general_deptos(self, fecha_ini, fecha_fin):
        ingresos_res = self.repo_ingresos.obtener_global_deptos(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)

        if not ingresos_res:
            raise ValueError(
                "No se Encontraron Ingresos por Departamentos (Respuesta vacía).")
        try:
            df = pd.DataFrame(ingresos_res)
        except Exception as e:
            raise ValueError(f"No se pudo convertir a DataFrame: {e}")
        if df.empty:
            raise ValueError(
                "No se Encontraron Ingresos por Departamentos  (DataFrame vacío).")
        return df

    def ingresos_diarios_catastro(self,  fecha_ini, fecha_fin):
        data_res = self.repo_ingresos.obtener_diario_catastro(
            fecha_ini=fecha_ini, fecha_fin=fecha_fin)

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

    def ingresos_diarios_tributaria_otras_tasas(self,  fecha_ini, fecha_fin):
        data_res = self.repo_ingresos.obtener_diario_ics_otras(
            fecha_ini=fecha_ini, fecha_fin=fecha_fin)

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

    def ingresos_diarios_tributaria_abonos(self,  fecha_ini, fecha_fin):
        data_res = self.repo_ingresos.obtener_diario_ics_abonos(
            fecha_ini=fecha_ini, fecha_fin=fecha_fin)

        if not data_res:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados De Abonos (respuesta vacía).")
        try:
            df = pd.DataFrame(data_res)
        except Exception as e:
            raise ValueError(
                f"No se pudo convertir a DataFrame: (Ingresos Diarios Pago De Abonos ) {e}")
        if df.empty:
            raise ValueError(
                "No se Encontraron Ingresos Diarios Detallados Pago De Abonos   (DataFrame vacío).")
        return df

    def ingresos_diarios_tributaria_inmuebles(self,  fecha_ini, fecha_fin):
        data_res = self.repo_ingresos.obtener_diario_ics_bienes(
            fecha_ini=fecha_ini, fecha_fin=fecha_fin)

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

    def ingresos_diarios_tributaria_comercio(self, fecha_ini, fecha_fin):
        data_res = self.repo_ingresos.obtener_diario_ics_comercio(
            fecha_ini=fecha_ini, fecha_fin=fecha_fin)

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

    def ingresos_diarios_tributaria_personal(self, fecha_ini, fecha_fin):
        data_res = self.repo_ingresos.obtener_diario_ics_personal(
            fecha_ini=fecha_ini, fecha_fin=fecha_fin)

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

    def ingresos_diarios_uma(self,  fecha_ini, fecha_fin):
        data_res = self.repo_ingresos.obtener_diario_uma(
            fecha_ini=fecha_ini, fecha_fin=fecha_fin)

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

    def ingresos_diarios_justicia(self,  fecha_ini, fecha_fin):
        data_res = self.repo_ingresos.obtener_diario_justicia(
            fecha_ini=fecha_ini, fecha_fin=fecha_fin)

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

    def ingresos_diarios_secretaria(self,  fecha_ini, fecha_fin):
        data_res = self.repo_ingresos.obtener_diario_secretaria(
            fecha_ini=fecha_ini, fecha_fin=fecha_fin)

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

    def ingresos_diarios_procamut(self,  fecha_ini, fecha_fin):
        data_res = self.repo_ingresos.obtener_diario_procamut(
            fecha_ini=fecha_ini, fecha_fin=fecha_fin)

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

    def ingresos_diarios_desarrollo_urbano(self,  fecha_ini, fecha_fin):
        data_res = self.repo_ingresos.obtener_diario_urbanizacion(
            fecha_ini=fecha_ini, fecha_fin=fecha_fin)

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

    def ingresos_semanal_uma(self,  fecha_ini, fecha_fin):
        data_res = self.repo_ingresos.obtener_semanal_uma(
            fecha_ini=fecha_ini, fecha_fin=fecha_fin)

        if not data_res:
            raise ValueError(
                "No se Encontraron Ingresos Semanales UMA (respuesta vacía).")
        try:
            df = pd.DataFrame(data_res)
        except Exception as e:
            raise ValueError(
                f"No se pudo convertir a DataFrame: (Ingresos Semanales UMA) {e}")
        if df.empty:
            raise ValueError(
                "No se Encontraron Ingresos Semanales UMA  (DataFrame vacío).")
        return df

    def ingresos_mensual_uma(self,  fecha_ini, fecha_fin):
        data_res = self.repo_ingresos.obtener_mensual_uma(
            fecha_ini=fecha_ini, fecha_fin=fecha_fin)

        if not data_res:
            raise ValueError(
                "No se Encontraron Ingresos Mensuales UMA (respuesta vacía).")
        try:
            df = pd.DataFrame(data_res)
        except Exception as e:
            raise ValueError(
                f"No se pudo convertir a DataFrame: (Ingresos Mensuales UMA) {e}")
        if df.empty:
            raise ValueError(
                "No se Encontraron Ingresos Mensuales UMA  (DataFrame vacío).")
        # Columnas numéricas (de la posición 3 a la 6)
        cols_sumar = df.columns[3:7]

        fila_total = {col: "" for col in df.columns}

        fila_total["Tipo"] = "TOTAL"

        for col in cols_sumar:
            fila_total[col] = df[col].sum()

        df.loc[len(df)] = fila_total

        return df
