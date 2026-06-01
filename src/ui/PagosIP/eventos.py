import flet as ft


def file_picker_result(vista, e: ft.FilePickerResultEvent):
    if not e.files:
        return

    ruta_excel = e.files[0].path
    vista.txt_ruta_excel.value = ruta_excel
    vista.txt_ruta_excel.update()

    # Aquí luego puedes cargar pandas
    # vista.cargar_excel(ruta_excel)
