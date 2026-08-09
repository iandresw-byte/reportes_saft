import flet as ft
from src.ui.components.ui_botones import create_boton_pdf, create_boton_salir_modal, create_boton_editar
from src.ui.components.ui_text import create_sub_titulo_modal, create_texFiel_fijas, create_titulo_modal
from src.ui.components.ui_colors import color_bg


def abrir_modal_licencia_ics_data(vista,data, e) -> ft.AlertDialog:

    def on_click_editar(e):
        txt_establecimiento.read_only = False
        vista.update()

    recibo_num = vista.num_recibo.current.value
    datos = data[0][0]
    print(datos)
    permiso = datos.get("id")
    txt_recibo = create_texFiel_fijas(
        "Numero de Recibo",value=recibo_num, ref=vista.num_recibo)
    txt_nombre = create_texFiel_fijas("Nombre Propietario",value=datos["propietario"])
    txt_identidad = create_texFiel_fijas("D.N.I.", value=datos["dni"])
    txt_establecimiento = create_texFiel_fijas("Nombre Establecimiento",value=datos["establecimiento"])
    txt_RTM = create_texFiel_fijas("R.T.M.",value=datos["rtm"])
    txt_direccion = create_texFiel_fijas("Direccion",value=datos["direccion_establecimento"])
    txt_fecha_solicitud = create_texFiel_fijas("Fecha Solicitud",value=datos["fecha_solicitud"])
    txt_fecha_vencimiento = create_texFiel_fijas("Nombre Inicio",value=datos["fecha_vence"])
    btn_editar = create_boton_editar()
    btn_editar.on_click = on_click_editar
    if not permiso:
        btn_editar.visible = False
    btn_liciencia = create_boton_pdf()
    btn_liciencia.on_click = vista.generar_pdf_licencia_ambiental_ics
    btn_salir = create_boton_salir_modal()
    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal(
        "TASA AMBIENTAL A ESTABLECIMEINTOS COMERCIALES")
    txt_sub_titulo = create_sub_titulo_modal(
        "Ingrese el numero de recibo con el que pago la tasa ambiental:")
    txt_sub_titulo_2 = create_sub_titulo_modal(
        "Datos Licencia Ambiental")
    
    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,
        content=ft.Column(
            controls=[
                ft.Divider(),
                txt_sub_titulo,
                txt_recibo,
                ft.Divider(),
                txt_sub_titulo_2,
                txt_identidad,
                txt_nombre,
                txt_RTM,
                txt_establecimiento,
                txt_direccion,
                txt_fecha_solicitud,
                txt_fecha_vencimiento,
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
            btn_liciencia,
            btn_editar,
            btn_salir
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
