
from datetime import datetime
from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
import pandas as pd

from src.reports.utils.analisis_ingresos_utils import ajuste_automatico_columnas, color_columa_diferencia, formato_celdas_moneda, formato_fecha, formato_mes, formato_titulo, formato_titulo_columna


class AnalisisIngresosReport:
    def __init__(self, datos: pd.DataFrame, municipio, titulo_reporte, anio):
        self.datos = datos
        self.municipio = municipio
        self.anio_act = anio
        self.anio_ant = int(anio) - 1
        self.titulo = titulo_reporte

    def generar_excel(self, ruta_salida="mora_vs_ingresos_gral.xlsx"):
        wb = Workbook()
        ws = wb.active
        if not ws:
            return
        ws.title = f"{self.anio_act} vs {self.anio_ant}"
        # ===============================
        # TITULO Y FECHA
        # ===============================
        titulo = f"{self.municipio['NombreMuni']} - {self.municipio['NombreDepto']}"
        titulo_rpt = f"ANALISIS DE INGRESOS - {self.anio_ant} vs {self.anio_act}"
        fecha = f"Fecha de elaboración: {datetime.now().strftime('%d/%m/%Y %H:%M')}"

        formato_titulo(ws, titulo ,"A1:AO1")
        formato_titulo(ws, titulo_rpt ,"A2:AO2")
        formato_fecha(ws, fecha, "A3:AO3")

        formato_mes(ws, "ENERO","C4:E4")
        formato_mes(ws, "FEBRERO","F4:H4")
        formato_mes(ws, "MARZO","I4:K4")
        formato_mes(ws, "ABRIL","L4:N4")
        formato_mes(ws, "MAYO","O4:Q4")
        formato_mes(ws, "JUNIO","R4:S4")
        formato_mes(ws, "JULIO","U4:W4")
        formato_mes(ws, "AGOSTO","X4:Z4")
        formato_mes(ws, "SEPTIEMBRE","AA4:AC4")
        formato_mes(ws, "OCTUBRE","AD4:AF4")
        formato_mes(ws, "NOVIEMBRE","AG4:AI4")
        formato_mes(ws, "DICIEMBRE","AJ4:AL4")
        formato_mes(ws, "RESUMEN ANUAL","AM4:AO4")

        fila_actual = 5  #Encabezados
        ws.freeze_panes = "A6"
        # ===============================
        # ENCABEZADOS
        # ===============================
        columnas = []
        for col in self.datos.columns:
            columnas.append(col,)
        formato_titulo_columna(ws,columnas,fila_actual)
        fila_actual += 1
        # ===============================
        # LLENADO DE DATOS
        # ===============================
        for index, item in self.datos.iterrows():
            ws.append([
                item["CODIGO"].strip(),
                item["NOMBRE CUENTA DE INGRESO"].strip(),
                item[f"INGRESOS ENERO [{self.anio_ant}]"],
                item[f"INGRESOS ENERO [{self.anio_act}]"],
                item["DIFERENCIA ENERO"],
                item[f"INGRESOS FEBRERO [{self.anio_ant}]"],
                item[f"INGRESOS FEBRERO [{self.anio_act}]"],
                item["DIFERENCIA FEBRERO"],
                item[f"INGRESOS MARZO [{self.anio_ant}]"],
                item[f"INGRESOS MARZO [{self.anio_act}]"],
                item["DIFERENCIA MARZO"],
                item[f"INGRESOS ABRIL [{self.anio_ant}]"],
                item[f"INGRESOS ABRIL [{self.anio_act}]"],
                item["DIFERENCIA ABRIL"],
                item[f"INGRESOS MAYO [{self.anio_ant}]"],
                item[f"INGRESOS MAYO [{self.anio_act}]"],
                item["DIFERENCIA MAYO"],
                item[f"INGRESOS JUNIO [{self.anio_ant}]"],
                item[f"INGRESOS JUNIO [{self.anio_act}]"],
                item["DIFERENCIA JUNIO"],
                item[f"INGRESOS JULIO [{self.anio_ant}]"],
                item[f"INGRESOS JULIO [{self.anio_act}]"],
                item["DIFERENCIA JULIO"],
                item[f"INGRESOS AGOSTO [{self.anio_ant}]"],
                item[f"INGRESOS AGOSTO [{self.anio_act}]"],
                item["DIFERENCIA AGOSTO"],
                item[f"INGRESOS SEPTIEMBRE [{self.anio_ant}]"],
                item[f"INGRESOS SEPTIEMBRE [{self.anio_act}]"],
                item["DIFERENCIA SEPTIEMBRE"],
                item[f"INGRESOS OCTUBRE [{self.anio_ant}]"],
                item[f"INGRESOS OCTUBRE [{self.anio_act}]"],
                item["DIFERENCIA OCTUBRE"],
                item[f"INGRESOS NOVIEMBRE [{self.anio_ant}]"],
                item[f"INGRESOS NOVIEMBRE [{self.anio_act}]"],
                item["DIFERENCIA NOVIEMBRE"],
                item[f"INGRESOS DICIEMBRE [{self.anio_ant}]"],
                item[f"INGRESOS DICIEMBRE [{self.anio_act}]"],
                item["DIFERENCIA DICIEMBRE"],
                item[F"TOTAL [{self.anio_ant}]"],
                item[F"TOTAL [{self.anio_act}]"],
                item["DIFERENCIA ANUAL"]
            ])
        # ===============================
        # FORMATO DE CELDAS Y MONEDA
        # ===============================
        ultima_fila = ws.max_row
        fila = 5
        formato_celdas_moneda(ws, primera_fila=fila,ultima_fila=ultima_fila,rango=F"A5:AO{ultima_fila}")
        # ===============================
        # AJUSTE AUTOMÁTICO DE COLUMNAS
        # ===============================
        ajuste_automatico_columnas(ws)
        color_columa_diferencia(ultima_fila, ws, "E")
        color_columa_diferencia(ultima_fila, ws, "H")
        color_columa_diferencia(ultima_fila, ws, "K")
        color_columa_diferencia(ultima_fila, ws, "N")
        color_columa_diferencia(ultima_fila, ws, "Q")
        color_columa_diferencia(ultima_fila, ws, "T")
        color_columa_diferencia(ultima_fila, ws, "W")
        color_columa_diferencia(ultima_fila, ws, "Z")
        color_columa_diferencia(ultima_fila, ws, "AC")
        color_columa_diferencia(ultima_fila, ws, "AF")
        color_columa_diferencia(ultima_fila, ws, "AI")
        color_columa_diferencia(ultima_fila, ws, "AL")
        color_columa_diferencia(ultima_fila, ws, "AO")
        # ===============================
        # GUARDAR
        # ===============================
        wb.save(ruta_salida)
        return ruta_salida

