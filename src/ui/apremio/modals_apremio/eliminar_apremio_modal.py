import flet as ft
from src.ui.components.ui_botones import create_boton_eliminar, create_boton_salir_modal
from src.ui.components.ui_text import create_sub_titulo_modal, create_titulo_modal, create_texFiel_fijas
from src.ui.components.ui_colors import color_bg
from src.ui.components.ui_checkBox import createCheckBox


def abrir_modal_eliminar_apremio(vista, id_documento):

    txt_titulo = create_titulo_modal("ELIMINAR PROCEDIMIENTO DE APREMIO")
    txt_sub_titulo = create_sub_titulo_modal(
        "Seleccione el motivo de la eliminación"
    )

    # motivos
    razon_1 = createCheckBox("Se va a recalcular la declaración.")
    razon_2 = createCheckBox("Error en el cargo de tasas.")
    razon_3 = createCheckBox("Error en el cargo de impuestos.")
    razon_4 = createCheckBox("Arreglo de pago.")
    razon_otro = createCheckBox("Otro")

    # campo otro (inicia oculto)
    txt_otro = create_texFiel_fijas(
        "Escriba otro motivo aquí...", read_only=False
    )
    txt_otro.visible = False
    divider = ft.Divider(visible=False)
    # 👉 mostrar/ocultar campo "otro"

    def toggle_otro(e):
        txt_otro.visible = razon_otro.value
        divider.visible = razon_otro.value
        vista.page.update()

    razon_otro.on_change = toggle_otro

    # 🔥 confirmar eliminación
    def confirmar_eliminacion(e):

        motivos = []

        if razon_1.value:
            motivos.append(razon_1.label)
        if razon_2.value:
            motivos.append(razon_2.label)
        if razon_3.value:
            motivos.append(razon_3.label)
        if razon_4.value:
            motivos.append(razon_4.label)

        if razon_otro.value and txt_otro.value:
            motivos.append(txt_otro.value)

        if not motivos:
            vista.page.snack_bar = ft.SnackBar(
                ft.Text("Debe seleccionar al menos un motivo.")
            )
            vista.page.snack_bar.open = True
            vista.page.update()
            return

        motivo_final = " | ".join(motivos)

        vista.eliminar_apremio(id_documento, motivo_final)
        vista.cerrar_modal()

    btn_eliminar = create_boton_eliminar()
    btn_eliminar.on_click = confirmar_eliminacion

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
                razon_1,
                razon_2,
                razon_3,
                razon_4,
                razon_otro,
                divider,
                txt_otro,
                ft.Divider(),
            ],
            tight=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        actions=[
            btn_eliminar,
            btn_salir
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
