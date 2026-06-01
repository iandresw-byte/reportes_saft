from reportlab.platypus import Table, Paragraph
from src.reports.utils.manejador_data_frame import sumar_ingresos_bomberos_sami, sumar_ingresos_bomberos_gobernacion
from src.ui.components.ui_style_table import columa_style, fila_style, fila_style_moneda, fila_style_moneda_total, table_style_UMA


def tabla_ingreso_detallado_bomberos(datos, tipo_cta=0) -> Table:
    estilo_encabezado = columa_style()
    estilo_fila = fila_style()
    estilo_tabla = table_style_UMA()
    estilo_fila_moneda = fila_style_moneda()
    estilo_fila_moneda_total = fila_style_moneda_total()
    encabezados = []
    encabezados.append(Paragraph("No.", estilo_encabezado),)
    if tipo_cta:
        datos = sumar_ingresos_bomberos_sami(datos)
    else:
        datos = sumar_ingresos_bomberos_gobernacion(datos)
    for col in datos.columns:
        encabezados.append(Paragraph(col, estilo_encabezado),)
    filas = [encabezados]
    for index, item in datos.iterrows():
        dni = item["DNI"].strip()
        num = str(item["No. Recibo"])
        if item["Nombre Completo"] == "Total":
            estilo_moneda = estilo_fila_moneda_total
            estilo_fila_nombre = estilo_fila_moneda_total
            no = ""
        else:
            estilo_moneda = estilo_fila_moneda
            estilo_fila_nombre = estilo_fila
            no = str(int(index)+1)
        if tipo_cta:
            filas.append([
                Paragraph(no, estilo_fila),
                Paragraph(num, estilo_fila),
                Paragraph(dni, estilo_fila),
                Paragraph(f'{item["Nombre Completo"]}', estilo_fila_nombre),
                Paragraph(f'{item["SALDO"]:,.2f}', estilo_moneda),
                Paragraph(
                    f'{item["RECUPERACION DE SALDOS"]:,.2f}',  estilo_moneda),
                Paragraph(f'{item["RECARGOS"]:,.2f}',   estilo_moneda),
                Paragraph(f'{item["INTERESES"]:,.2f}', estilo_moneda),
                Paragraph(f'{item["TOTAL"]:,.2f}', estilo_moneda),
            ])
        else:
            filas.append([
                Paragraph(no, estilo_fila),
                Paragraph(num, estilo_fila),
                Paragraph(dni, estilo_fila),
                Paragraph(f'{item["Nombre Completo"]}', estilo_fila_nombre),
                Paragraph(f'{item["SALDO"]:,.2f}', estilo_moneda),
                Paragraph(
                    f'{item["RECUPERACION DE SALDOS"]:,.2f}',  estilo_moneda),
                Paragraph(f'{item["TOTAL"]:,.2f}', estilo_moneda),
            ])
    if tipo_cta:
        tabla = Table(filas, colWidths=[
            30, 50, 80, 180, 70, 70, 70, 70, 70])
    else:
        tabla = Table(filas, colWidths=[
            30, 50, 80, 180, 70, 70, 70])
    tabla.setStyle(estilo_tabla)
    return tabla
