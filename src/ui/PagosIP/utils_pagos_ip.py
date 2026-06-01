

import asyncio
import logging
import os
import pandas as pd
import webbrowser
from src.ui.components.ui_snack_bar import snack_error, snack_inicio, snack_rpt_generado


def snack_inicio_reporte(page, mensaje, e: None):
    if e:
        e.control.disabled = True
    page.open(snack_inicio(mensaje))
    page.update()


def snack_final_reporte(page, nombre, e):
    e.control.disabled = False
    page.open(snack_rpt_generado(nombre))
    page.update()


def snack_error_reporte(page, error):
    logging.error(f"Error Generar Reporte: {error}", exc_info=True)
    page.open(snack_error(str(error)))
    page.update()


async def ejecutar_reporte(
    vista,
    e,
    nombre_archivo,
    obtener_datos,
    construir_reporte=None,
    tipo="pdf",
):
    ruta = os.path.join(os.getcwd(), nombre_archivo)

    try:
        snack_inicio_reporte(
            vista.page, f"Iniciando reporte: {nombre_archivo}", e)
        await asyncio.sleep(0.5)

        # 👇 función que retorna los datos
        datos = obtener_datos()

        if isinstance(datos, pd.DataFrame):
            is_data = len(datos) > 0
        else:
            is_data = datos is not None

        if is_data:
            # 👇 función que retorna la instancia del reporte
            reporte = construir_reporte(datos)  # type: ignore

        # 👇 genera el archivo correspondiente
            if tipo == "pdf":
                reporte.generar_pdf(ruta)
            elif tipo == "excel":
                ruta = reporte.generar_excel()

            snack_final_reporte(vista.page, nombre_archivo, e)
            await asyncio.sleep(0.5)

        # 👇 Abrir archivo
            if tipo == "pdf":
                webbrowser.open_new_tab(f"file://{ruta}")
            else:
                os.startfile(ruta)
        else:
            snack_error_reporte(vista.page, "Sin datos para mostarar")

    except Exception as ex:
        snack_error_reporte(vista.page, ex)
