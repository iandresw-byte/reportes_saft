from flet import Alignment, Column, Container, BoxShadow, Colors, CrossAxisAlignment, FontWeight, Icon, Icons, MainAxisAlignment, Offset, Animation, AnimationCurve, Text, TextAlign

from src.ui.components.ui_radio import create_radio


def create_boton_tamanio_pdf(label_text="Nombre de\nla Constancia", icono=Icons.DESCRIPTION_OUTLINED, on_click=None,
                             tooltip=None,
                             data=None,
                             Ref=None,
                             Key=None,
                            color_icono="#2E7D32",
                            color_tarjeta="#FFFFFF",
                            color_circulo="#C8E6C9",
                            color_texto="#1B5E20"):
    print(Key)
    return Container(
        data=data,
        width=140,
        height=160,
        key=Key,
        ref=Ref,
        border_radius=20,
        bgcolor=color_tarjeta,
        tooltip=tooltip,
        ink=True,
        shadow=BoxShadow(
            spread_radius=1,
            blur_radius=12,
            color=Colors.BLACK26,
            offset=Offset(2, 4),
        ),
        animate=Animation(200, AnimationCurve.EASE_OUT),
        content=Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=12,
            controls=[
                Container(
                    width=80,
                    height=80,
                    border_radius=40,
                    bgcolor=color_circulo,
                    alignment=Alignment(0, 0),
                    content=Icon(
                        icono,
                        size=42,
                        color=color_icono
                    ),
                ),
                Text(
                    label_text,
                    text_align=TextAlign.CENTER,
                    size=16,
                    weight=FontWeight.BOLD,
                    color=color_texto,
                ),
                
            ],
        ),
        on_click=on_click,
    )
