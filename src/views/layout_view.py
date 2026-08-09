import flet as ft
import os
from src.views.permiso_operacion_view import VistaPermisoOperacion
from src.views.about_view import VistaAbout
from src.services.parametro_service import ParametroService
from src.ui.reports.vista_reportes import VistaReportes
from src.ui.apremio.vista_apremio import VistaApremio
from src.ui.PagosIP.vista import VistaPagosIP
from src.views.no_disponible_view import VistaNoDisponible
from src.ui.dashboard.vista_dashboard import VistaDashBoard
from src.ui.constancias.vista import VistaConstancias
from src.ui.ajustes.vista_ajustes import VistaAjustesPO
from src.ui.PagosIP.eventos import file_picker_result
from src.ui.components.ui_colors import color_bg, color_bg_2, color_shadow, color_texto
from src.ui.components.ui_container import create_container_rail


class UILayout(ft.Container):
    def __init__(self, page: ft.Page, context, logger):
        super().__init__(expand=True)
        self._page = page
        page.update()
        self.x_width = 4200
        self.x_height = 4200
        self._page.window.max_height = self.x_height
        self._page.window.min_height = None
        self._page.window.max_width = self.x_width
        self._page.window.min_width = None
        page.update()
        self._page.window.maximizable = True
        self._page.window.minimizable = True
        self._page.window.maximizable = True
        self._page.window.resizable = True
        self._page.title = "Reportes SAFT"
        self._page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self._page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self._page.padding = 15
        self._page.update()
        self.context = context

        self.context.init_saft()

        self._page.window.icon = "assets/images/icon.ico"
       
        text_color = color_texto()
        bg_color = color_bg()
        bg_2_color = color_bg_2()
        shadow_color = color_shadow()
        self.context.datos_muni = self.context.administracion_service.obtener_datos_municipalidad()
        self.context.datos_admin = self.context.administracion_service.obtener_datos_municipalidad_admin()
        self.context.datos_system = self.context.administracion_service.obtener_datos_systema()
        self.user = self.context.usuario_actual

        municipalidad = self.context.municipio = self.context.datos_muni['NombreMuni'].rstrip(
        )
        departamento = self.context.departamento = self.context.datos_muni['NombreDepto'].rstrip(
        )
        # --- Título superior ---
        self.titulo_muni = ft.Text(f"{municipalidad} - {departamento}",
                                   size=24,
                                   weight=ft.FontWeight.BOLD,
                                   text_align=ft.TextAlign.CENTER,
                                   color=text_color
                                   )
        user = self.user.username

        self.user_info = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(
                    content=ft.Text("Cerrar sesión",
                                    color=color_texto()),
                    on_click=lambda e: self.cerrar_sesion(), height=20),
            ],
            content=ft.Row(
                [
                    ft.CircleAvatar(
                        content=ft.Image(src='/images/avatar.png',
                                         width=40, height=40),
                        radius=16,
                        bgcolor="#4A90E2",
                    ),
                    ft.Text(
                        user,
                        color=color_texto(),
                        size=14,
                        weight=ft.FontWeight.BOLD
                    )
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.END,

            ),
            menu_position=ft.PopupMenuPosition.UNDER,
            bgcolor=color_bg_2())

    # --- Crear las vistas ---
        self.views = {
            "reportes": lambda: VistaReportes(self._page, self.context).build(),
            "pagos_ip": lambda: VistaPagosIP(self._page, self.context).build(),
            "permiso": lambda: VistaPermisoOperacion(self._page, self.context).build(),
            "ajustes": lambda: VistaAjustesPO(self._page, self.context).build(),
            "about": lambda: VistaAbout(self._page, self.context).build(),
            "apremio": lambda: VistaApremio(self._page, self.context).build(),
            "no_disponible": lambda: VistaNoDisponible(self._page, self.context).build(),
            "constancias": lambda: VistaConstancias(self._page, self.context).build()
        }

        self.main_content = ft.Container(
            expand=1,
            content=self.views["reportes"]()
        )
        super_admin = self.user.tiene_modulo('SE')
        user_po = self.user.validar_permiso("CT", "CkPo")
        user_pagos_empresa = self.user.validar_permiso("CT", "ChkDipe")
    # --- Función para cambiar vista según selección ---

        def on_nav_change(e):
            index = e.control.selected_index

            if index == 0:
                self.main_content.content = self.views["reportes"]()
            elif index == 1:
                if user_po:
                    self.main_content.content = self.views["permiso"]()
                else:
                    self.main_content.content = self.views["no_disponible"]()
            elif index == 2:
                self.main_content.content = self.views["apremio"]()
            elif index == 3:
                if user_pagos_empresa:
                    self.main_content.content = self.views["pagos_ip"]()
                else:
                    self.main_content.content = self.views["no_disponible"]()
            elif index == 4:
                if super_admin:
                    self.main_content.content = self.views["ajustes"]()
                else:
                    self.main_content.content = self.views["no_disponible"]()
            elif index == 5:
                self.main_content.content = self.views["constancias"]()

            elif index == 6:
                self.main_content.content = self.views["about"]()

            self._page.update()

        # --- Menú lateral (NavigationRail) ---
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            indicator_color=bg_color,
            indicator_shape=ft.RoundedRectangleBorder(radius=5),
            selected_label_text_style=ft.TextStyle(),
            bgcolor=bg_2_color,
            leading=ft.Image(src="/images/saft.png", width=50),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    visible=False,
                    icon=ft.Icon(ft.Icons.SPACE_DASHBOARD_OUTLINED,
                                 color=text_color, size=20),
                    selected_icon=ft.Icon(
                        ft.Icons.SPACE_DASHBOARD_ROUNDED, color=text_color, size=20),
                    label_content=ft.Text("Dashbord",  color=text_color,
                                          size=11, text_align=ft.TextAlign.CENTER),
                    indicator_color=shadow_color,

                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.VIEW_COMFORTABLE_OUTLINED,
                                 color=text_color, size=20),
                    selected_icon=ft.Icon(
                        ft.Icons.VIEW_COMFORTABLE_ROUNDED, color=text_color, size=20),
                    label_content=ft.Text(
                        "Reportes",  color=text_color, size=11, text_align=ft.TextAlign.CENTER),
                    indicator_color=shadow_color,
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.ADD_HOME_WORK_OUTLINED,
                                 color=text_color, size=20),
                    selected_icon=ft.Icon(
                        ft.Icons.ADD_HOME_WORK_ROUNDED, color=text_color, size=20),
                    label_content=ft.Text(
                        "Permiso Operación.", color=text_color, size=11, text_align=ft.TextAlign.CENTER),
                    indicator_color=shadow_color,
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.LAYERS_OUTLINED,
                                 color=text_color, size=20),
                    selected_icon=ft.Icon(
                        ft.Icons.LAYERS_ROUNDED, color=text_color, size=20),
                    label_content=ft.Text(
                        "Proceso de Apremio", color=text_color, size=11, text_align=ft.TextAlign.CENTER),
                    indicator_color=shadow_color,
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.SETTINGS_ACCESSIBILITY_OUTLINED,
                                 color=text_color, size=20),
                    selected_icon=ft.Icon(
                        ft.Icons.SETTINGS_ACCESSIBILITY_ROUNDED, color=text_color, size=20),
                    label_content=ft.Text(
                        "Pagos IP.", color=text_color, size=11, text_align=ft.TextAlign.CENTER),
                    indicator_color=shadow_color,
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.SETTINGS_SUGGEST_OUTLINED,
                                 color=text_color, size=20),
                    selected_icon=ft.Icon(
                        ft.Icons.SETTINGS_SUGGEST_ROUNDED, color=text_color, size=20),
                    label_content=ft.Text(
                        "Ajustes", color=text_color, size=11, text_align=ft.TextAlign.CENTER),
                    indicator_color=shadow_color,
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.FACT_CHECK,
                                 color=text_color, size=20),
                    selected_icon=ft.Icon(
                        ft.Icons.VERIFIED, color=text_color, size=20),
                    label_content=ft.Text(
                        "Constancias", color=text_color, size=11, text_align=ft.TextAlign.CENTER),
                    indicator_color=shadow_color,
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.ARCHIVE_OUTLINED,
                                 color=text_color, size=20),
                    selected_icon=ft.Icon(
                        ft.Icons.ARCHIVE_ROUNDED, color=text_color, size=20),
                    label_content=ft.Text(
                        "Acerca De", color=text_color, size=11, text_align=ft.TextAlign.CENTER),
                    indicator_color=shadow_color,
                ),
            ],
            on_change=on_nav_change,
        )

        self.con_rail = create_container_rail(
            content=rail,
            expand=False
        )
        # --- Fondo principal ---
        self._page.bgcolor = bg_color

    def build(self):  # type: ignore
        return ft.Column(
            [
                ft.Row([self.titulo_muni, self.user_info],
                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row(
                    [
                        self.con_rail,
                        ft.VerticalDivider(width=2),
                        self.main_content,  # donde se muestran las vistas
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )

    def cerrar_sesion(self):
        self._page.window.close()
        self._page.window.destroy()  # Cierra la ventana completa
        os._exit(0)
