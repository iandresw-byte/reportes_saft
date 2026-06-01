from reportlab.platypus import Table, Paragraph
from src.reports.utils.manejador_data_frame import sumar_ingresos_departo_admin_tributaria_os
from src.reports.utils.manejador_data_depto_mensual import sumar_ingresos_depto_mensual_admin_tributaria_os
from src.reports.utils.manejador_data_depto_diario_frame import sumar_ingresos_depto_diarios_admin_tributaria_os
from src.ui.components.ui_style_table import columa_style, fila_style, fila_style_moneda, fila_style_moneda_total, table_style_UMA


def tabla_ingreso_detallado_admin_tributaria_os(datos, ) -> Table:
    estilo_encabezado = columa_style()
    estilo_fila = fila_style()
    estilo_tabla = table_style_UMA()
    estilo_fila_moneda = fila_style_moneda()
    estilo_fila_moneda_total = fila_style_moneda_total()
    encabezados = []
    encabezados.append(Paragraph("No.", estilo_encabezado),)
    datos = sumar_ingresos_departo_admin_tributaria_os(datos)
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

        filas.append([
            Paragraph(no, estilo_fila),
            Paragraph(num, estilo_fila),
            Paragraph(dni, estilo_fila),
            Paragraph(f'{item["Nombre Completo"]}', estilo_fila_nombre),
            Paragraph(f'{item["Impuestos"]:,.2f}',   estilo_moneda),
            Paragraph(f'{item["Servicios"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Constancias"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Certificaciones"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Documentacion"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Otros"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Total Recibo"]:,.2f}', estilo_moneda)
        ])

    tabla = Table(filas, colWidths=[
        25, 40, 72, 150, 75, 50, 48, 48, 48, 48, 48])
    tabla.setStyle(estilo_tabla)
    return tabla


def tabla_ingreso_diario_admin_tributaria_os(datos, ) -> Table:
    estilo_encabezado = columa_style()
    estilo_fila = fila_style()
    estilo_tabla = table_style_UMA()
    estilo_fila_moneda = fila_style_moneda()
    estilo_fila_moneda_total = fila_style_moneda_total()
    encabezados = []
    encabezados.append(Paragraph("No.", estilo_encabezado),)
    datos = sumar_ingresos_depto_diarios_admin_tributaria_os(datos)
    for col in datos.columns:
        encabezados.append(Paragraph(col, estilo_encabezado),)
    filas = [encabezados]
    for index, item in datos.iterrows():
        if item["Fecha"] == "Total":
            estilo_moneda = estilo_fila_moneda_total
            no = ""
        else:
            estilo_moneda = estilo_fila_moneda
            no = str(int(index)+1)

        filas.append([
            Paragraph(no, estilo_fila),
            Paragraph(f'{item["Fecha"]}', estilo_moneda),
            Paragraph(f'{item["Impuestos"]:,.2f}',   estilo_moneda),
            Paragraph(f'{item["Servicios"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Constancias"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Certificaciones"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Documentacion"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Otros"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Total"]:,.2f}', estilo_moneda)
        ])

    tabla = Table(filas, colWidths=[
        25, 60, 70, 70, 70, 70, 70, 70, 70])
    tabla.setStyle(estilo_tabla)
    return tabla


def tabla_ingreso_mensual_admin_tributaria_os(datos, ) -> Table:
    estilo_encabezado = columa_style()
    estilo_fila = fila_style()
    estilo_tabla = table_style_UMA()
    estilo_fila_moneda = fila_style_moneda()
    estilo_fila_moneda_total = fila_style_moneda_total()
    encabezados = []
    encabezados.append(Paragraph("No.", estilo_encabezado),)
    datos = sumar_ingresos_depto_mensual_admin_tributaria_os(datos)
    for col in datos.columns:
        encabezados.append(Paragraph(col, estilo_encabezado),)
    filas = [encabezados]
    for index, item in datos.iterrows():
        if item["Mes"] == "Total":
            estilo_moneda = estilo_fila_moneda_total
            no = ""
        else:
            estilo_moneda = estilo_fila_moneda
            no = str(int(index)+1)

        filas.append([
            Paragraph(no, estilo_fila),
            Paragraph(f'{item["Mes"]}', estilo_moneda),
            Paragraph(f'{item["Impuestos"]:,.2f}',   estilo_moneda),
            Paragraph(f'{item["Servicios"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Constancias"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Certificaciones"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Documentacion"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Otros"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Total"]:,.2f}', estilo_moneda)
        ])

    tabla = Table(filas, colWidths=[
        25, 60, 70, 70, 70, 70, 70, 70, 70])
    tabla.setStyle(estilo_tabla)
    return tabla


def tabla_ingreso_detallado_admin_excel_tributaria_os(excel, datos, ws):
    for index, item in datos.iterrows():
        ixd = index+1
        nombre_completo = item["Nombre Completo"]
        num = item["No. Recibo"]
        excel.fila_num += 1
        ws.append([
            ixd,
            num,
            item["DNI"].strip(),
            nombre_completo,
            f'{item["Impuestos"]:,.2f}',
            f'{item["Servicios"]:,.2f}',
            f'{item["Constancias"]:,.2f}',
            f'{item["Certificaciones"]:,.2f}',
            f'{item["Documentacion"]:,.2f}',
            f'{item["Otros"]:,.2f}',
            f'{item["Total Recibo"]:,.2f}',
        ])
    return ws


def tabla_ingreso_diario_admin_excel_tributaria_os(excel, datos, ws):
    for index, item in datos.iterrows():
        ixd = index+1
        excel.fila_num += 1
        ws.append([
            ixd,
            item["Fecha"],
            f'{item["Impuestos"]:,.2f}',
            f'{item["Servicios"]:,.2f}',
            f'{item["Constancias"]:,.2f}',
            f'{item["Certificaciones"]:,.2f}',
            f'{item["Documentacion"]:,.2f}',
            f'{item["Otros"]:,.2f}',
            f'{item["Total"]:,.2f}',
        ])
    return ws
