from flet import ElevatedButton, ButtonStyle, TextStyle, Icons, BorderSide, RoundedRectangleBorder
from src.ui.components.ui_colors import color_bg_2, color_borde, color_shadow, color_texto


def create_boton(text_label="hola", on_click=None, width=200, disabled=False):
    borde_color = color_borde()
    txt_color = color_texto()
    shadow_color = color_shadow()
    return ElevatedButton(
        text_label,
        disabled=disabled,
        width=width,
        color=txt_color,
        style=ButtonStyle(
            side=BorderSide(2, borde_color),
            shape=RoundedRectangleBorder(radius=18),
            bgcolor=color_bg_2(),
            shadow_color=shadow_color,
            text_style=TextStyle(size=10, font_family="Tahoma"),
        ),
        on_click=on_click,
    )


def create_boton_icono(text_label="hola", on_click=None, width=200, disabled=False):
    borde_color = color_borde()
    txt_color = color_texto()
    shadow_color = color_shadow()
    return ElevatedButton(
        text_label,
        disabled=disabled,
        width=width,
        color=txt_color,
        style=ButtonStyle(
            side=BorderSide(2, borde_color),
            shape=RoundedRectangleBorder(radius=18),
            bgcolor=color_bg_2(),
            shadow_color=shadow_color,
            text_style=TextStyle(size=10, font_family="Tahoma"),
        ),
        on_click=on_click,
    )


def crear_boton_excel() -> ElevatedButton:
    return ElevatedButton(
        "Excel",
        width=80,
        icon=Icons.BACKUP_TABLE_ROUNDED,
        color=color_borde(),
        style=ButtonStyle(
            side=BorderSide(2, color_borde()),
            shape=RoundedRectangleBorder(radius=18),
            bgcolor=color_bg_2(),
            shadow_color=color_shadow(),
            text_style=TextStyle(
                size=11, font_family="Tahoma", color=color_borde()),
        )
    )


def create_boton_pdf() -> ElevatedButton:
    return ElevatedButton("PDF", icon=Icons.PICTURE_AS_PDF_OUTLINED,
                          color=color_borde(),
                          width=80,
                          style=ButtonStyle(
                              side=BorderSide(2, color_borde()),
                              shape=RoundedRectangleBorder(
                                  radius=18),
                              bgcolor=color_bg_2(),
                              shadow_color=color_shadow(),
                              text_style=TextStyle(
                                  size=11, font_family="Tahoma", color=color_borde()),
                          ))


def create_boton_salir_modal() -> ElevatedButton:
    return ElevatedButton("Salir", icon=Icons.EXIT_TO_APP, color=color_borde(),
                          width=80,
                          style=ButtonStyle(
        side=BorderSide(2, color_borde()),
        shape=RoundedRectangleBorder(
            radius=18),
        bgcolor=color_bg_2(),
        shadow_color=color_shadow(),
        text_style=TextStyle(
            size=11, font_family="Tahoma", color=color_borde()),
    ),
    )


def create_boton_aceptar(ancho=80) -> ElevatedButton:
    return ElevatedButton("Aceptar", icon=Icons.CACHED, color=color_borde(),
                          width=ancho,
                          style=ButtonStyle(
        side=BorderSide(2, color_borde()),
        shape=RoundedRectangleBorder(
            radius=18),
        bgcolor=color_bg_2(),
        shadow_color=color_shadow(),
        text_style=TextStyle(
            size=11, font_family="Tahoma", color=color_borde()),
    ),
    )


def create_boton_guardar_modal() -> ElevatedButton:
    return ElevatedButton("Guardar", icon=Icons.SAVE_AS_OUTLINED, color=color_borde(),
                          width=90,
                          style=ButtonStyle(
        side=BorderSide(2, color_borde()),
        shape=RoundedRectangleBorder(
            radius=18),
        bgcolor=color_bg_2(),
        shadow_color=color_shadow(),
        text_style=TextStyle(
            size=11, font_family="Tahoma", color=color_borde()),
    ),
    )


def create_boton_reiniciar_modal() -> ElevatedButton:
    return ElevatedButton("Reiniciar", icon=Icons.SYNC_OUTLINED, color=color_borde(),
                          width=90,
                          style=ButtonStyle(
        side=BorderSide(2, color_borde()),
        shape=RoundedRectangleBorder(
            radius=18),
        bgcolor=color_bg_2(),
        shadow_color=color_shadow(),
        text_style=TextStyle(
            size=11, font_family="Tahoma", color=color_borde()),
    ),
    )


def create_boton_eliminar() -> ElevatedButton:
    return ElevatedButton("Eliminar", icon=Icons.DELETE, color=color_texto(),
                          width=90,
                          style=ButtonStyle(
                              side=BorderSide(2, color_borde()),
                              shape=RoundedRectangleBorder(
                                  radius=18),
                              bgcolor=color_bg_2(),
                              shadow_color=color_shadow(),
                              text_style=TextStyle(
                                  size=11, font_family="Tahoma", color=color_borde()),
    ),
    )
