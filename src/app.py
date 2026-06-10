# src/app.py

import asyncio
import flet as ft
from src.services.update_services import UpdateService  # type: ignore
from src.views.splash_view import SplashView
from src.views.login_view import PantallaLogin
from src.views.updater_view import PantallaActualizacion
from src.contexts.app_context import AppContext
from src.utils.logger_config import configurar_logger
from src.utils.validar_version import validar_version


async def app(page: ft.Page):
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

    # Simula carga
    await asyncio.sleep(2)

    log = configurar_logger()

    context = AppContext()
    context.init_services()
    actualizador = UpdateService(page)
    actualizado = actualizador.verificar_actualizacion_inicio(None)

    page.clean()

    if not actualizado:
        login = PantallaLogin(page, context, log)
        page.add(await login.build())
    else:
        page.add(PantallaActualizacion(page, ))

    page.update()
