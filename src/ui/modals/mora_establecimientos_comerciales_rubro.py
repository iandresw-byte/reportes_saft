import flet as ft
from datetime import date
from src.ui.components.ui_radio import rd_tipo_rubro_ics
from src.ui.components.ui_dropbox import dropbox_cuentas_ingreso
from src.ui.components.ui_calendario import create_fecha
from src.ui.components.ui_botones import create_boton_pdf, create_boton_salir_modal, crear_boton_excel
from src.ui.components.ui_text import create_sub_titulo_modal, create_titulo_modal, create_texFiel_fijas
from src.ui.components.ui_colors import color_bg, color_texto
texto_color = color_texto()


def abrir_modal_establecimientos_comerciales_rubro(vista, e):

    vista.cuenta_ics_ref = ft.Ref[ft.Dropdown]()
    vista.cod_aldea = ft.Ref[ft.Dropdown]()
    vista.cod_barrio = ft.Ref[ft.Dropdown]()
    tipo_cta = ft.Ref[ft.RadioGroup]()

    fecha = date.today()
    anio, mes = fecha.year, fecha.month
    
    
    
    cuentas = vista.cuentas_ics
    def handle_cuentas(e):
        cuenta = e.data
        for row_cuenta in cuentas:
            if row_cuenta["CtaIngreso"] == cuenta:
                vista.cuenta_ics = row_cuenta
                break

    def handle_tipo_ics(e):
        cuentas_seccionada = []
        tipo = e.data
        if tipo == "0":
            for cuenta in cuentas:
                if cuenta["CtaIngreso"][0:6] == '117101':
                    cuentas_seccionada.append(cuenta)
        elif tipo == "1":
            for cuenta in cuentas:
                if cuenta["CtaIngreso"][0:6] == '117102':
                    cuentas_seccionada.append(cuenta)
        elif tipo == "2":
            for cuenta in cuentas:
                if cuenta["CtaIngreso"][0:6] == '117102':
                    cuentas_seccionada.append(cuenta)
        else:
            cuentas_seccionada = cuentas
        
        dropbox_cuentas_ics.options = [ft.dropdown.Option(
            data = a,
            key=a["CtaIngreso"],
            text=a["NombreCtaIngreso"],
            text_style=ft.TextStyle(
                size=10, font_family="Tahoma", color=texto_color),
            style=ft.ButtonStyle(color=texto_color, text_style=ft.TextStyle(
                size=10, font_family="Tahoma", color=texto_color)))
            for  a in cuentas_seccionada]
        
        dropbox_cuentas_ics.update()
        
    dropbox_cuentas_ics = dropbox_cuentas_ingreso(cuentas=cuentas,ref=vista.cuenta_ics_ref)
    dropbox_cuentas_ics.on_change = handle_cuentas

    rd_tipo_ics = rd_tipo_rubro_ics(tipo=tipo_cta)
    rd_tipo_ics.on_change = handle_tipo_ics


    btn_pdf = create_boton_pdf()
    btn_pdf.on_click = vista.generar_reporte_mora_establecimiento_por_actividad_pdf

    btn_excel = crear_boton_excel()
    btn_excel.on_click = vista.generar_reporte_mora_establecimiento_por_actividad_excel

    btn_salir = create_boton_salir_modal()

    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal(
        "Mora Establecimeintos Comerciales por Actividad Economica")
    txt_sub_titulo = create_sub_titulo_modal("Seleccione la Actividad Economica")

    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,
        content=ft.Column(
            controls=[
                ft.Divider(),
                txt_sub_titulo,
                ft.Divider(),
                rd_tipo_ics,
                dropbox_cuentas_ics,
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
