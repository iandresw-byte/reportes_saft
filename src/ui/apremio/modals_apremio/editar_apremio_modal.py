import flet as ft
from datetime import date
import calendar

from src.ui.components.ui_botones import (
    create_boton_guardar_modal,
    create_boton_reiniciar_modal,
    create_boton_salir_modal
)
from src.ui.components.ui_text import (
    create_sub_titulo_modal,
    create_titulo_modal,
    create_texFiel_fijas
)
from src.ui.components.ui_colors import color_bg
from src.ui.components.ui_radio import rd_estado_editar, rd_tipo_entrega_apremio
from src.ui.components.ui_calendario import create_fecha


def abrir_modal_editar_apremio(vista, fila):

    # ========= FECHA =========
    fecha = date.today()
    anio, mes = fecha.year, fecha.month
    ultimo_dia = calendar.monthrange(anio, mes)[1]

    vista.proceso = ft.Ref[ft.RadioGroup]()
    vista.tipo_entrega = ft.Ref[ft.RadioGroup]()
    radio_estado = rd_estado_editar(vista.proceso)

    # ========= TITULOS =========
    txt_titulo = create_titulo_modal("EDITAR PROCEDIMIENTO DE APREMIO")
    txt_sub_titulo = create_sub_titulo_modal("Marcar documento como entregado")
    txt_sub_titulo_2 = create_sub_titulo_modal("Reiniciar paso")
    txt_sub_titulo_2.size = 12
    txt_sub_titulo.size = 12

    # ========= CAMPOS FIJOS =========
    saldo_ini = create_texFiel_fijas(
        "Saldo Al Inicio del Proceso", value=fila["Monto_ini_formateado"], width=300)
    saldo_actual = create_texFiel_fijas(
        "Saldo Actual", value=fila["Monto_act_formateado"], width=300)

    saldo_en_pp = create_texFiel_fijas(
        "Saldo en Plan de Pago", value=fila["Monto_plan_pago_formateado"], width=300)
    saldo_anulado = create_texFiel_fijas(
        "Saldo Anulado", value=fila["Monto_anulado_formateado"], width=300)
    saldo_pagado = create_texFiel_fijas(
        "Saldo Pagado", value=fila["Monto_pagado_formateado"])

    tipo_impuesto = create_texFiel_fijas(
        "Tipo Impuesto", value=fila["TipoImpDescripcionLong"])
    txt_movimiento = create_texFiel_fijas(
        "Movimientos", value=fila["estado"], read_only=True)
    txt_observaciones = create_texFiel_fijas(
        "Observaciones", value=fila["Observacion"].replace("|", "\n"), read_only=True)
    txt_observaciones.multiline = True
    txt_observaciones.height = None

    # ========= FECHA ENTREGA =========
    def handle_change_fecha(e):
        vista.fecha_entrega = e.control.value.strftime('%Y%m%d')
        fecha_entrega.text = e.control.value.strftime('%d-%m-%Y')
        fecha_entrega.update()

    def handle_dismissal(e):
        fecha_entrega.text = date(anio, mes, 1).strftime('%d/%m/%Y')
        fecha_entrega.update()

    fecha_entrega = create_fecha(
        vista,
        "Fecha de Entrega",
        vista.fecha_entrega,
        handle_change_fecha,
        handle_dismissal
    )

    fecha_generado = create_fecha(
        vista,
        "Fecha de Generado",
        vista.fecha_generado,
        handle_change_fecha,
        handle_dismissal
    )
    fecha_generado.tooltip = "Fecha de Generacion de Requerimiento"
    # ========= BOTONES =========
    btn_guardar = create_boton_guardar_modal()

    btn_reiniciar = create_boton_reiniciar_modal()
    btn_reiniciar.visible = False

    btn_salir = create_boton_salir_modal()
    btn_salir.on_click = lambda _: vista.cerrar_modal()

    # ========= MOTIVOS =========

    rd_entrega = rd_tipo_entrega_apremio(vista.tipo_entrega)

    txt_otro = create_texFiel_fijas("Describa otro aquí...", read_only=False)

    txt_otro.visible = False
    divider_otro = ft.Divider(visible=False)

    # ========= ESTADOS =========
    estado_editar = ft.Column(
        controls=[
            txt_sub_titulo,
            ft.Divider(),
            ft.Row([fecha_entrega], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            rd_entrega,
            divider_otro,
            txt_otro,
            ft.Divider(),

            ft.Row(controls=[btn_guardar, btn_salir],
                   alignment=ft.MainAxisAlignment.SPACE_AROUND)
        ], alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    estado_reiniciar = ft.Column(
        controls=[
            txt_sub_titulo_2,
            ft.Divider(),
            tipo_impuesto,
            ft.Row(controls=[saldo_ini,
                             saldo_actual,],
                   alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ft.Row(controls=[saldo_en_pp,
                             saldo_anulado,],
                   alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ft.Row([saldo_pagado, fecha_generado],
                   alignment=ft.MainAxisAlignment.CENTER),

            txt_movimiento,

            ft.Divider(),
            ft.Row(controls=[btn_reiniciar, btn_salir],
                   alignment=ft.MainAxisAlignment.SPACE_AROUND)
        ],
        visible=False,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # ========= ACCIONES =========
    def cambiar_estado(e):
        modo = vista.proceso.current.value

        editando = modo == "editar"

        estado_editar.visible = editando
        estado_reiniciar.visible = not editando

        if not editando:
            fecha_generado.text = fila["FechaFormateadaGenerada"]
            fecha_generado.disabled = not editando

        btn_guardar.visible = editando
        btn_reiniciar.visible = not editando

        vista.page.update()

    def cambiar_entrega(e):
        modo = vista.tipo_entrega.current.value

        entrega = modo == "4"

        txt_otro.visible = entrega
        divider_otro.visible = entrega
        vista.page.update()

        vista.page.update()

    # ========= CONFIRMAR =========

    def confirmar_edicion(e):
        motivo_final = get_tipo_entrega(vista.tipo_entrega.current.value)

        if not motivo_final:
            vista.page.snack_bar = ft.SnackBar(
                ft.Text("Debe seleccionar al menos un motivo."))
            vista.page.snack_bar.open = True
            vista.page.update()
            return

        vista.editar_apremio(fila["IdDocumento"],
                             vista.fecha_entrega, motivo_final)
        vista.cerrar_modal()

    def confirmar_reinicio(e):
        vista.reiniciar_apremio(fila, e)
        vista.cerrar_modal()

    def get_tipo_entrega(tipo_entrega):
        if tipo_entrega == '0':
            return "Entregado Personalmente"
        elif tipo_entrega == '1':
            return "Entregado a un tercero"
        elif tipo_entrega == '2':
            return "Notificado (Se dejó en la propiedad)"
        elif tipo_entrega == '3':
            return "Notificado en la Municipalidad"
        elif tipo_entrega == '4':
            return "Otros"
        else:
            return ""

    btn_reiniciar.on_click = confirmar_reinicio
    rd_entrega.on_change = cambiar_entrega
    radio_estado.on_change = cambiar_estado
    btn_guardar.on_click = confirmar_edicion
    # ========= DIALOG =========
    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,
        content=ft.Column(
            controls=[
                radio_estado,
                estado_editar,
                estado_reiniciar,
                txt_observaciones,
            ],
            tight=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        actions=[],
        actions_alignment=ft.MainAxisAlignment.SPACE_AROUND,
    )
