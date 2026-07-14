import flet as ft
from src.ui.components.ui_botones import create_boton_aceptar, create_boton_salir_modal
from src.ui.components.ui_calendario import create_fecha
from src.ui.components.ui_text import create_sub_titulo_modal, create_titulo_modal, create_texFiel_fijas
from src.ui.components.ui_colors import color_bg
from src.ui.components.ui_table import table_identifiacion_facturacion_pp, table_identifiacion_cuota_pp


def abrir_modal_anular_pp(vista, resultado, df_cuotas, df_facturas, pla_pago, callback):
    txt_titulo = create_titulo_modal("ANULAR PLAN DE PAGO")
    txt_sub_titulo = create_sub_titulo_modal(
        "Datos del Contribuyente"
    )
    txt_sub_titulo_1 = create_sub_titulo_modal(
        "Datos del Plan de Pago"
    )
    txt_sub_titulo_2 = create_sub_titulo_modal(
        "Datos de Facturacion"
    )
    txt_nota_mora = create_sub_titulo_modal(
        "Para obtener datos actualizados consulte la identidad \n del contribuyente en el Modulo de Admnistracion Tributaria en Atencion al Cliente."
    )

    def anular_pp(e):
        callback("ACEPTAR")
        vista.cerrar_modal()

    def cancelar_pp(e):
        callback("CANCELAR")
        vista.cerrar_modal()

    # motivos
    txt_nombre = create_texFiel_fijas(label_text="Nombre Contribuyente",value=pla_pago.loc[0,"Nombre_Completo"])
    txt_dni = create_texFiel_fijas(label_text="Nombre Contribuyente",value=pla_pago.loc[0,"Identidad"])
    txt_valor_pagado = create_texFiel_fijas(label_text="Valor Cuotas Pagadas",value=resultado["total_pp_pagado"])
    txt_valor_vencido = create_texFiel_fijas(label_text="Valor Cuotas Vencidas",value=resultado["total_pp_vencido"])
    txt_valor_vigente = create_texFiel_fijas(label_text="Valor Cuotas Vigetes",value=resultado["total_pp_vigente"])
    txt_valor = create_texFiel_fijas(label_text="Valor Plan Pago Pagado",value=resultado["total_pp_pagado_tentativo"])
    txt_valor_FPnPP = create_texFiel_fijas(label_text="Saldo Facturas Cubre Plan de Pago",value=resultado["total_fnp_cubre"])
    txt_valor_FRnPPN= create_texFiel_fijas(label_text="Saldo Facturas No El Cubre Plan de Pago",value=resultado["total_fnp_no_cubre"])
    txt_valor_residuo_pago= create_texFiel_fijas(label_text="Residuo Sumado A la Ultima Fcatura que Consevrva estado",value=resultado["total_residuo_pagado"])
    txt_valor_no_residuo_pago= create_texFiel_fijas(label_text="Residuo Restado a la Primer Fcatura Activada",value=resultado["total_residuo_vencido"])
    
    txt_mod_fatura_add= create_texFiel_fijas(label_text="Ultima Factura Conserva Estado",value=resultado["num_avpg_add"])
    txt_mod_fatura_res= create_texFiel_fijas(label_text="Primer Factura Activada",value=resultado["num_avpg_res"])
    

    btn_salir = create_boton_salir_modal()
    btn_salir.on_click = cancelar_pp


    btn_aceptar = create_boton_aceptar()
    btn_aceptar.on_click = anular_pp



    tabla_cuotas_pp = table_identifiacion_cuota_pp(vista, df_cuotas)
    tabla_facturas_pp = table_identifiacion_facturacion_pp(vista, df_facturas)


    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,
        content=ft.Column(
            controls=[
                txt_sub_titulo,
                ft.Divider(),
                txt_dni,
                txt_nombre,
                txt_sub_titulo_1,
                ft.Divider(),
                ft.Row([txt_valor_pagado, txt_valor_vencido, txt_valor_vigente]),
                ft.Row([txt_valor_FPnPP, txt_valor_FRnPPN, txt_valor]),
                ft.Row([txt_mod_fatura_add, txt_valor_residuo_pago]),
                ft.Row([txt_mod_fatura_res, txt_valor_no_residuo_pago]),
                txt_nota_mora,
                txt_sub_titulo_2,
                ft.Divider(),
                tabla_cuotas_pp,
                ft.Divider(),
                tabla_facturas_pp,
                ft.Divider(),
            ],
            tight=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        actions=[
            btn_aceptar,
            btn_salir
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
