import flet as ft
from src.ui.components.ui_botones import create_boton_salir_modal
from src.ui.components.ui_calendario import create_fecha
from src.ui.components.ui_text import create_sub_titulo_modal, create_titulo_modal, create_texFiel_fijas
from src.ui.components.ui_colors import color_bg
from src.ui.components.ui_table import color_estado_proceso


def abrir_modal_ver_apremio(vista, fila_data):
    txt_titulo = create_titulo_modal("PROCEDIMIENTO DE APREMIO")
    txt_sub_titulo = create_sub_titulo_modal(
        "Datos del Requerido"
    )
    txt_nota_mora = create_sub_titulo_modal(
        "Para obtener datos actualizados consulte la identidad \n del contribuyente en el Modulo de Admnistracion Tributaria en Atencion al Cliente."
    )

    # motivos
    txt_identidad = create_texFiel_fijas(
        "D.N.I.", value=fila_data['DNI_Formateado'])
    txtNombre = create_texFiel_fijas(
        "Nombre Completo", value=fila_data['NombreCompleto'])

    saldo_ini = create_texFiel_fijas(
        "Saldo Al Inicio del Proceso", value=fila_data["Monto_ini_formateado"])
    saldo_actual = create_texFiel_fijas(
        "Saldo Actual", value=fila_data["Monto_act_formateado"])

    saldo_en_pp = create_texFiel_fijas(
        "Saldo en Plan de Pago", value=fila_data["Monto_plan_pago_formateado"])
    saldo_anulado = create_texFiel_fijas(
        "Saldo Anulado", value=fila_data["Monto_anulado_formateado"])
    saldo_pagado = create_texFiel_fijas(
        "Saldo Pagado", value=fila_data["Monto_pagado_formateado"])
    visible_1er = fila_data["TipoDoc"] == 1
    visible_2do = fila_data["TipoDoc"] == 2
    visible_3er = fila_data["TipoDoc"] == 3
    if "TipoDocDescripcion1er" in fila_data and fila_data["TipoDocDescripcion1er"]:
        color_estado1er = color_estado_proceso(fila_data["Estado1er"])

        documento1er = create_texFiel_fijas(
            value=fila_data["TipoDocDescripcion1er"]
        )

        estado1er = create_texFiel_fijas(
            "Estado Proceso",
            value=fila_data["Estado1er"],
            color=color_estado1er
        )
        estado1er.border_color = color_estado1er
    else:
        documento1er = create_texFiel_fijas("None", visible=False)
        estado1er = create_texFiel_fijas("None", visible=False)
    if "TipoDocDescripcion2do" in fila_data and fila_data["TipoDocDescripcion2do"]:
        color_estado2do = color_estado_proceso(fila_data["Estado2do"])

        documento2do = create_texFiel_fijas(
            value=fila_data["TipoDocDescripcion2do"]
        )

        estado2do = create_texFiel_fijas(
            "Estado Proceso",
            value=fila_data["Estado2do"],
            color=color_estado2do
        )
        estado2do.border_color = color_estado2do
    else:
        documento2do = create_texFiel_fijas("None", visible=False)
        estado2do = create_texFiel_fijas("None", visible=False)
    if "TipoDocDescripcion3er" in fila_data and fila_data["TipoDocDescripcion3er"]:
        color_estado3er = color_estado_proceso(fila_data["Estado3er"])

        documento3er = create_texFiel_fijas(
            value=fila_data["TipoDocDescripcion3er"]
        )

        estado3er = create_texFiel_fijas(
            "Estado Proceso",
            value=fila_data["Estado3er"],
            color=color_estado3er
        )
        estado3er.border_color = color_estado3er
    else:
        documento3er = create_texFiel_fijas("None", visible=False)
        estado3er = create_texFiel_fijas("None", visible=False)

    # if visible_1er:
    #     documento.visible = True
    #     documento2do.visible = True
    #     documento3er.visible = True
    #     estado.visible = True
    #     estado2do.visible = True
    #     estado3er.visible = True
    # elif visible_2do:
    #     documento.visible = False
    #     documento2do.visible = True
    #     documento3er.visible = True
    #     estado.visible = False
    #     estado2do.visible = True
    #     estado3er.visible = True
    # elif visible_3er:
    #     documento.visible = False
    #     documento2do.visible = False
    #     documento3er.visible = True
    #     estado.visible = False
    #     estado2do.visible = False
    #     estado3er.visible = True

    saldo_pagado = create_texFiel_fijas(
        "Saldo Pagado", value=fila_data["Monto_pagado_formateado"])

    tipo_impuesto = create_texFiel_fijas(
        "Tipo Impuesto", value=fila_data["TipoImpDescripcionLong"])
    txt_movimiento = create_texFiel_fijas(
        "Movimientos", value=fila_data["estado"], read_only=True)
    txt_observaciones = create_texFiel_fijas(
        "Observaciones", value=fila_data["Observacion"].replace("|", "\n"), read_only=True)
    txt_observaciones.multiline = True
    txt_observaciones.height = None
    fecha_generado = create_fecha(
        vista,
        "Fecha de Generado",
        None,
        None,
        None
    )
    fecha_generado.tooltip = "Fecha de Generacion de Requerimiento"
    fecha_generado.text = fila_data["FechaFormateadaGenerada"]

    fecha_entregado = create_fecha(
        vista,
        "Fecha de Entrega",
        None,
        None,
        None
    )
    fecha_entregado.tooltip = "Fecha de Entrega de Requerimiento"
    fecha_entregado.text = fila_data["FechaFormateadaEntrega"]

    btn_salir = create_boton_salir_modal()
    btn_salir.on_click = lambda _: vista.cerrar_modal()

    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,
        content=ft.Column(
            controls=[
                txt_sub_titulo,
                ft.Divider(),
                txt_identidad,
                txtNombre,
                ft.Row(controls=[tipo_impuesto, fecha_generado],
                       alignment=ft.MainAxisAlignment.SPACE_AROUND),

                ft.Divider(),
                ft.Row(controls=[saldo_ini, saldo_actual,],
                       alignment=ft.MainAxisAlignment.SPACE_AROUND),
                ft.Row(controls=[saldo_en_pp, saldo_anulado, saldo_pagado],
                       alignment=ft.MainAxisAlignment.SPACE_AROUND),
                txt_movimiento,
                txt_nota_mora,
                ft.Divider(),
                ft.Row([documento1er, estado1er, fecha_entregado],
                       alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([documento2do, estado2do],
                       alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([documento3er, estado3er],
                       alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(),
                txt_observaciones,

                ft.Divider(),
            ],
            tight=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        actions=[
            btn_salir
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
