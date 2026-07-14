import flet as ft
from datetime import date
from src.ui.components.ui_radio import rd_tipo_persona
from src.ui.components.ui_dropbox import dropbox_cuentas_ingreso
from src.ui.components.ui_calendario import create_fecha
from src.ui.components.ui_botones import create_boton_pdf, create_boton_salir_modal, crear_boton_excel
from src.ui.components.ui_text import create_sub_titulo_modal, create_titulo_modal, create_texFiel_fijas
from src.ui.components.ui_colors import color_bg, color_texto
texto_color = color_texto()


def abrir_modal_abonados_x_servicio(vista, e):

    vista.cuenta_sp = ft.Ref[ft.Dropdown]()
    vista.cod_aldea = ft.Ref[ft.Dropdown]()
    vista.cod_barrio = ft.Ref[ft.Dropdown]()

    fecha = date.today()
    anio, mes = fecha.year, fecha.month

    cuentas = vista.cuentas_sp
    def handle_cuentas_sp(e):
      
        
        cuenta_sp = e.data
    
        for cuenta in cuentas:
            if cuenta["CtaIngreso"] == cuenta_sp:
                vista.cuenta_sp = cuenta
                break




    dropbox_cuentas_sp = dropbox_cuentas_ingreso(cuentas=cuentas,ref=vista.cuenta_sp)
    dropbox_cuentas_sp.on_change = handle_cuentas_sp
    btn_pdf = create_boton_pdf()
    btn_pdf.on_click = vista.generar_reporte_mora_abonado_por_cuenta_pdf

    btn_excel = crear_boton_excel()
    btn_excel.on_click = vista.generar_reporte_mora_abonado_por_cuenta_excel

    btn_salir = create_boton_salir_modal()

    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal(
        "ABONADO POR TIPO DE SERVICIO")
    txt_sub_titulo = create_sub_titulo_modal("Seleccione un servicio")

    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,
        content=ft.Column(
            controls=[
                ft.Divider(),
                txt_sub_titulo,
                ft.Divider(),
                dropbox_cuentas_sp,
                ft.Divider(),
            ],
            tight=True,
            scroll=ft.ScrollMode.AUTO,
            col=12,
            alignment=ft.MainAxisAlignment.CENTER,         # centra verticalmente
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centra horizontalmente
            expand=True
        ),
        actions=[
            btn_pdf,
            btn_excel,
            btn_salir
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
