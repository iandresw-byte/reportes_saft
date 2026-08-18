# src/app.py

import asyncio
import flet as ft
from src.services.update_services import UpdateService  # type: ignore
from src.views.splash_view import SplashView
from src.views.login_view import PantallaLogin
from src.views.updater_view import PantallaActualizacion, PantallaActualizacionBD
from src.contexts.app_context import AppContext
from src.utils.logger_config import configurar_logger
import os
import time
import psutil


_proceso = psutil.Process(os.getpid())
_inicio = time.perf_counter()


def medir_memoria(nombre):
    memoria = _proceso.memory_info().rss / 1024 / 1024
    tiempo = time.perf_counter() - _inicio

    print(
        f"[{tiempo:8.2f}s] "
        f"{nombre:<35} "
        f"RAM: {memoria:8.2f} MB"
    )

async def app(page: ft.Page):
    medir_memoria("Inicio")
    x_width = 720
    x_height = 440

    page.title = "SAFT"
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.maximizable = False
    page.window.minimizable = False
    page.window.resizable = False
    page.window.width = x_width
    page.window.height = x_height
    page.window.max_height = x_height
    page.window.min_height = x_height
    page.window.max_width = x_width
    page.window.min_width = x_width
    page.window.center()
    page.update()

    splash = SplashView()

    page.add(splash)
    page.update()
    medir_memoria("Después configuración Flet")
    # Simula carga
    await asyncio.sleep(2)

    log = configurar_logger()

    context = AppContext()
    context.init_services()
    context.init_app()
    medir_memoria("Después conexión SQL")
    try:
        #assert context.administracion_service is not None
        #parametros = context.administracion_service.obtener_datos_municipalidad()
        #if not  parametros["VersionDB"]:
         #   print("Actualize base de datos")

        actualizador = UpdateService(page)
        actualizado = actualizador.verificar_actualizacion_inicio(context)
    
        page.clean()
    
        if not actualizado:
            login = PantallaLogin(page, context, log)
            page.add(await login.build())
        else:
            page.add(PantallaActualizacion(page, ))
    
        page.update()
        medir_memoria("Después crear interfaz")
    except:
        page.clean()
        page.add(PantallaActualizacionBD(page, ))
        page.update()

    
    
