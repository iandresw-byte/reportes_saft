from flet import DatePicker, ElevatedButton, BorderSide, Icons, ButtonStyle, TextStyle
from datetime import date
from src.ui.components.ui_colors import color_texto, color_bg_2


def create_fecha(self, label, ref, on_change, on_dismiss) -> ElevatedButton:
    texto_color = color_texto()
    bg_color = color_bg_2()
    fecha = date.today()
    anio = fecha.year
    mes = fecha.month
    return ElevatedButton(
        label,
        width=130,
        icon=Icons.CALENDAR_MONTH,
        style=ButtonStyle(
            side=BorderSide(2, texto_color),
            bgcolor=bg_color,
            color=texto_color,
            text_style=TextStyle(
                size=10,
                font_family="Tahoma",
                color=texto_color
            )
        ),
        on_click=lambda e: self.page.open(
            DatePicker(
                ref=ref,
                first_date=date(2000, 1, 1),
                last_date=date(year=anio, month=mes+1, day=1),
                on_change=on_change,
                on_dismiss=on_dismiss,
            )
        ),
    )
