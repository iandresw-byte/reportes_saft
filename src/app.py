import flet as ft
from src.views.login_view import PantallaLogin
from src.contexts.app_context import AppContext
from src.utils.logger_config import configurar_logger


async def app(page: ft.Page):
    page.title = "Login SAFT"
    page.window.icon = "assets/icon.ico"
    log = configurar_logger()
    context = AppContext()
    context.init_services()

    login_view = PantallaLogin(page, context, log)
    page.add(await login_view.build())  # type: ignore
