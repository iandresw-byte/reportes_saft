from flet import Page, ElevatedButton, Icons, ButtonStyle, TextStyle, Alignment, Colors, Border, BorderSide, Container
from src.ui.components.ui_colors import color_bg,  color_shadow


def create_update_button(page: Page, on_click=None):
    return Container(
        border=Border(top=BorderSide(2, Colors.BLUE_700), right=BorderSide(
            2, Colors.BLUE_700), left=BorderSide(2, Colors.BLUE_700), bottom=BorderSide(2, Colors.BLUE_700)),
        border_radius=18,
        content=ElevatedButton(
            "Actualizar aplicación",
            icon=Icons.SYSTEM_UPDATE,
            color=Colors.BLUE_700,
            width=200,
            style=ButtonStyle(bgcolor=color_bg(),
                              shadow_color=color_shadow(),
                              text_style=TextStyle(
                                  size=10,
                                  italic=False,
                                  font_family="Tahoma",
            ), alignment=Alignment(0, 0)),
            on_click=on_click)
    )

def actualizar_base_boton() -> ElevatedButton:
    return ElevatedButton(
        "Actualizar Base de Datos",
        icon=Icons.REBASE_EDIT,
        color=Colors.GREEN_700,
        visible=True,
        width=200,
        height=35,
        style=ButtonStyle(
            side=BorderSide(2, Colors.GREEN_700),
            bgcolor='#1b263b',
            shadow_color=Colors.GREEN_700,
            text_style=TextStyle(
                    size=10,
                    italic=False,
                    font_family="Tahoma",
                    color=Colors.GREEN_700,
            ),
            alignment=Alignment(0, 0),
        ))
