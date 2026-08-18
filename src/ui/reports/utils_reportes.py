

import asyncio
import logging
import os
import time
import pandas as pd
import flet as ft
import webbrowser
from src.utils.config_manager import Config
from src.ui.components.ui_snack_bar import snack_error, snack_inicio, snack_rpt_generado
RESULTADO_DIR = Config.obtener("RUTAS", "carpeta_reportes")


def snack_inicio_reporte(page, mensaje, e):
    if isinstance(e, ft.ControlEvent ):
        e.control.disabled = False
    page.open(snack_inicio(mensaje))
    page.update()


def snack_final_reporte(page, nombre, e):
    if isinstance(e, ft.ControlEvent ):
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
    tiempo_datos=0
    tiempo_pdf=0
    tiempo_excel=0
    if RESULTADO_DIR:
        carpeta_pdf = os.path.join(RESULTADO_DIR, tipo)
        os.makedirs(carpeta_pdf, exist_ok=True)
        ruta = os.path.join(carpeta_pdf, nombre_archivo)
    else:
        carpeta_pdf = os.path.join(os.getcwd(), "res", tipo)
        os.makedirs(carpeta_pdf, exist_ok=True)
        ruta = os.path.join(carpeta_pdf, nombre_archivo)

    try:
        snack_inicio_reporte(
            vista.page, f"Iniciando reporte: {nombre_archivo}", e)
        await asyncio.sleep(0.5)

        # 👇 función que retorna los datos
        inicio = time.perf_counter()
        datos = obtener_datos()
        tiempo_datos += time.perf_counter() - inicio
        if isinstance(datos, pd.DataFrame):
            is_data = len(datos) > 0
        elif isinstance(datos, list):
            is_data = len(datos) > 0
        else:
            is_data = datos is not None

        if is_data:
            # 👇 función que retorna la instancia del reporte
            reporte = construir_reporte(datos)  # type: ignore
            if nombre_archivo == "licencia_uma_ics.pdf":
                vista.licencia_ambiental = datos

        # 👇 genera el archivo correspondiente
            if tipo == "pdf":
                inicio = time.perf_counter()
                reporte.generar_pdf(ruta)
                tiempo_pdf += time.perf_counter() - inicio
                
            elif tipo == "excel":
                inicio = time.perf_counter()
                ruta = reporte.generar_excel(ruta)
                tiempo_excel += time.perf_counter() - inicio
            snack_final_reporte(vista.page, nombre_archivo, e)
            await asyncio.sleep(0.5)

        # 👇 Abrir archivo
            if tipo == "pdf":
                webbrowser.open_new_tab(f"file://{ruta}")
            else:
                os.startfile(ruta)

            print(f"tiempo_datos:    {tiempo_datos:.2f} segundos")
            print(f"tiempo_pdf:     {tiempo_pdf:.2f} segundos")
            print(f"tiempo_excel:     {tiempo_excel:.2f} segundos")
        else:
            snack_error_reporte(vista.page, "Sin datos para mostarar")

    except Exception as ex:
        snack_error_reporte(vista.page, ex)
