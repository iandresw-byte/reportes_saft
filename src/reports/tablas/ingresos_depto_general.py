from reportlab.platypus import Table, Paragraph
from src.reports.utils.manejador_data_frame import sumar_ingresos_generales_depto
from src.ui.components.ui_style_table import columa_style, fila_style, fila_style_moneda, fila_style_moneda_total, table_style_UMA


def tabla_ingresos_generales_depto(datos, ) -> Table:
    estilo_encabezado = columa_style()
    estilo_fila = fila_style()
    estilo_tabla = table_style_UMA()
    estilo_fila_moneda = fila_style_moneda()
    estilo_fila_moneda_total = fila_style_moneda_total()
    encabezados = []
    encabezados.append(Paragraph("No.", estilo_encabezado),)
    datos = sumar_ingresos_generales_depto(datos)
    for col in datos.columns:
        encabezados.append(Paragraph(col, estilo_encabezado),)
    filas = [encabezados]
    for index, item in datos.iterrows():

        if item["DEPARTAMENTO - UNIDAD"] == "Total":
            estilo_moneda = estilo_fila_moneda_total
            estilo_fila_nombre = estilo_fila_moneda_total
            no = ""
        else:
            estilo_moneda = estilo_fila_moneda
            estilo_fila_nombre = estilo_fila
            no = str(int(index)+1)

        filas.append([
            no,
            Paragraph(f'{item["DEPARTAMENTO - UNIDAD"]}', estilo_fila_nombre),
            Paragraph(f'{item["INGRESOS"]:,.2f}', estilo_moneda),

        ])

    tabla = Table(filas, colWidths=[
        25, 200, 72])
    tabla.setStyle(estilo_tabla)
    return tabla
