import pandas as pd
from src.repositories.analisis_ingresos_repository import AnalisisIngresosRepository
from src.services.parametro_service import ParametroService


class AnalisisIngresosService:
    def __init__(self, conexion, sistem):
        self.reposicion = AnalisisIngresosRepository(conexion)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem

    def analisis_ingresos_anio_act_anio_ant(self, anio: int):
        data = self.reposicion.analisis_ingresos_anio_act_anio_ant(anio)
        if not data:
            raise ValueError(
                "No se encontraron datos de mora general de aldeas (respuesta vacía).")
        try:
            df = pd.DataFrame(data)
            df = self.sumar_analisis_data_frame(df, anio=int(anio)-1, anio_fin=int(anio))
        except Exception as e:
            raise ValueError(f"No se pudo convertir a DataFrame: {e}")
        if df.empty:
            raise ValueError(
                "No se encontraron datos de mora general de aldeas  (DataFrame vacío).")
        return df

    def sumar_analisis_data_frame(self, datos:pd.DataFrame, anio:int|None, anio_fin:int|None):
        datos["diferencia_enero"] = datos["enero_act"].fillna(0) - datos["enero_ant"].fillna(0)
        datos["diferencia_febrero"] = datos["febrero_act"].fillna(0) - datos["febrero_ant"].fillna(0)
        datos["diferencia_marzo"] = datos["marzo_act"].fillna(0) - datos["marzo_ant"].fillna(0)
        datos["diferencia_abril"] = datos["abril_act"].fillna(0) - datos["abril_ant"].fillna(0)
        datos["diferencia_mayo"] = datos["mayo_act"].fillna(0) - datos["mayo_ant"].fillna(0)
        datos["diferencia_junio"] = datos["junio_act"].fillna(0) - datos["junio_ant"].fillna(0)
        datos["diferencia_julio"] = datos["julio_act"].fillna(0) - datos["julio_ant"].fillna(0)
        datos["diferencia_agosto"] = datos["agosto_act"].fillna(0) - datos["agosto_ant"].fillna(0)
        datos["diferencia_septiembre"] = datos["septiembre_act"].fillna(0) - datos["septiembre_ant"].fillna(0)
        datos["diferencia_octubre"] = datos["octubre_act"].fillna(0) - datos["octubre_ant"].fillna(0)
        datos["diferencia_noviembre"] = datos["noviembre_act"].fillna(0) - datos["noviembre_ant"].fillna(0)
        datos["diferencia_diciembre"] = datos["diciembre_act"].fillna(0) - datos["diciembre_ant"].fillna(0)

        datos["total_anterior"] = datos[[
                "enero_ant",
                "febrero_ant",
                "marzo_ant",
                "abril_ant",
                "mayo_ant",
                "junio_ant",
                "julio_ant",
                "agosto_ant",
                "septiembre_ant",
                "octubre_ant",
                "noviembre_ant",
                "diciembre_ant",
                ]].sum(axis=1)
        datos["total_actual"] = datos[[
                "enero_act",
                "febrero_act",
                "marzo_act",
                "abril_act",
                "mayo_act",
                "junio_act",
                "julio_act",
                "agosto_act",
                "septiembre_act",
                "octubre_act",
                "noviembre_act",
                "diciembre_act",
                ]].sum(axis=1)

        datos["diferencia_anual"] = datos["total_actual"].fillna(0) - datos["total_anterior"].fillna(0)
        
        fila_total = {
                    "cta": "",
                    "Descripcion": "Total",
                    "enero_ant": datos["enero_ant"].sum(),
                    "enero_act": datos["enero_act"].sum(),
                    "febrero_ant": datos["febrero_ant"].sum(),
                    "febrero_act": datos["febrero_act"].sum(),
                    "marzo_ant": datos["marzo_ant"].sum(),
                    "marzo_act": datos["marzo_act"].sum(),
                    "abril_ant": datos["abril_ant"].sum(),
                    "abril_act": datos["abril_act"].sum(),
                    "mayo_ant":  datos["mayo_ant"].sum(),
                    "mayo_act":  datos["mayo_act"].sum(),
                    "junio_ant": datos["junio_ant"].sum(),
                    "junio_act": datos["junio_act"].sum(),
                    "julio_ant": datos["julio_ant"].sum(),
                    "julio_act": datos["julio_act"].sum(),
                    "agosto_ant": datos["agosto_ant"].sum(),
                    "agosto_act": datos["agosto_act"].sum(),
                    "septiembre_ant": datos["septiembre_ant"].sum(),
                    "septiembre_act": datos["septiembre_act"].sum(),
                    "octubre_ant": datos["octubre_ant"].sum(),
                    "octubre_act": datos["octubre_act"].sum(),
                    "noviembre_ant": datos["noviembre_ant"].sum(),
                    "noviembre_act": datos["noviembre_act"].sum(),
                    "diciembre_ant": datos["diciembre_ant"].sum(),
                    "diciembre_act": datos["diciembre_act"].sum(),
                    "diferencia_enero": datos["diferencia_enero"].sum(),
                    "diferencia_febrero": datos["diferencia_febrero"].sum(),
                    "diferencia_marzo": datos["diferencia_marzo"].sum(),
                    "diferencia_abril": datos["diferencia_abril"].sum(),
                    "diferencia_mayo": datos["diferencia_mayo"].sum(),
                    "diferencia_junio": datos["diferencia_junio"].sum(),
                    "diferencia_julio": datos["diferencia_julio"].sum(),
                    "diferencia_agosto": datos["diferencia_agosto"].sum(),
                    "diferencia_septiembre": datos["diferencia_septiembre"].sum(),
                    "diferencia_octubre": datos["diferencia_octubre"].sum(),
                    "diferencia_noviembre": datos["diferencia_noviembre"].sum(),
                    "diferencia_diciembre": datos["diferencia_diciembre"].sum(),
                    "total_anterior": datos["total_anterior"].sum(),
                    "total_actual": datos["total_actual"].sum(),
                    "diferencia_anual": datos["diferencia_anual"].sum(),
                          }
        datos.loc[len(datos)] = fila_total




        nuevo_df = datos[[
                "cta",
                "Descripcion",
                "enero_ant",
                "enero_act",
                "diferencia_enero",
                "febrero_ant",
                "febrero_act",
                "diferencia_febrero",
                "marzo_ant",
                "marzo_act",
                "diferencia_marzo",
                "abril_ant",
                "abril_act",
                "diferencia_abril",
                "mayo_ant",
                "mayo_act",
                "diferencia_mayo",
                "junio_ant",
                "junio_act",
                "diferencia_junio",
                "julio_ant",
                "julio_act",
                "diferencia_julio",
                "agosto_ant",
                "agosto_act",
                "diferencia_agosto",
                "septiembre_ant",
                "septiembre_act",
                "diferencia_septiembre",
                "octubre_ant",
                "octubre_act",
                "diferencia_octubre",
                "noviembre_ant",
                "noviembre_act",
                "diferencia_noviembre",
                "diciembre_ant",
                "diciembre_act",
                "diferencia_diciembre",
                "total_anterior",
                "total_actual",
                "diferencia_anual",
        ]]







        nuevo_df.columns = [
            "CODIGO",
            "NOMBRE CUENTA DE INGRESO",
            f"INGRESOS ENERO [{anio}]",
            f"INGRESOS ENERO [{anio_fin}]",
            "DIFERENCIA ENERO",
            f"INGRESOS FEBRERO [{anio}]",
            f"INGRESOS FEBRERO [{anio_fin}]",
            "DIFERENCIA FEBRERO",
            f"INGRESOS MARZO [{anio}]",
            f"INGRESOS MARZO [{anio_fin}]",
            "DIFERENCIA MARZO",
            f"INGRESOS ABRIL [{anio}]",
            f"INGRESOS ABRIL [{anio_fin}]",
            "DIFERENCIA ABRIL",
            f"INGRESOS MAYO [{anio}]",
            f"INGRESOS MAYO [{anio_fin}]",
            "DIFERENCIA MAYO",
            f"INGRESOS JUNIO [{anio}]",
            f"INGRESOS JUNIO [{anio_fin}]",
            "DIFERENCIA JUNIO",
            f"INGRESOS JULIO [{anio}]",
            f"INGRESOS JULIO [{anio_fin}]",
            "DIFERENCIA JULIO",
            f"INGRESOS AGOSTO [{anio}]",
            f"INGRESOS AGOSTO [{anio_fin}]",
            "DIFERENCIA AGOSTO",
            f"INGRESOS SEPTIEMBRE [{anio}]",
            f"INGRESOS SEPTIEMBRE [{anio_fin}]",
            "DIFERENCIA SEPTIEMBRE",
            f"INGRESOS OCTUBRE [{anio}]",
            f"INGRESOS OCTUBRE [{anio_fin}]",
            "DIFERENCIA OCTUBRE",
            f"INGRESOS NOVIEMBRE [{anio}]",
            f"INGRESOS NOVIEMBRE [{anio_fin}]",
            "DIFERENCIA NOVIEMBRE",
            f"INGRESOS DICIEMBRE [{anio}]",
            f"INGRESOS DICIEMBRE [{anio_fin}]",
            "DIFERENCIA DICIEMBRE",
            F"TOTAL [{anio}]",
            F"TOTAL [{anio_fin}]",
            "DIFERENCIA ANUAL"
        ]
        
        return nuevo_df
