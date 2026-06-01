from reportlab.platypus import Table, Paragraph
from src.reports.utils.manejador_data_frame import sumar_ingresos_depto_urbanizacion
from src.reports.utils.manejador_data_depto_diario_frame import sumar_ingresos_depto_diarios_urbanizacion
from src.reports.utils.manejador_data_depto_mensual import sumar_ingresos_depto_mensual_urbanizacion
from src.ui.components.ui_style_table import columa_style, fila_style, fila_style_moneda, fila_style_moneda_total, table_style_UMA


def tabla_ingreso_detallado_desarrollo_urbano(datos, ) -> Table:
    estilo_encabezado = columa_style()
    estilo_fila = fila_style()
    estilo_tabla = table_style_UMA()
    estilo_fila_moneda = fila_style_moneda()
    estilo_fila_moneda_total = fila_style_moneda_total()
    encabezados = []
    encabezados.append(Paragraph("No.", estilo_encabezado),)
    datos = sumar_ingresos_depto_urbanizacion(datos)
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
            Paragraph(
                f'{item["Autorizaciones"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Licencias para Ejercer"]:,.2f}',
                      estilo_moneda),
            Paragraph(f'{item["Permisos de Construcción"]:,.2f}',
                      estilo_moneda),
            Paragraph(
                f'{item["Permisos de Construcción de Antenas"]:,.2f}', estilo_moneda),
            Paragraph(
                f'{item["Instlación de Rótulos"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Constancias"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Otros"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Total Recibo"]:,.2f}', estilo_moneda)
        ])

    tabla = Table(filas, colWidths=[
        30, 40, 75, 160, 50, 50, 50, 50, 50, 50, 50,  50])
    tabla.setStyle(estilo_tabla)
    return tabla


def tabla_ingreso_diario_desarrollo_urbano(datos, ) -> Table:
    estilo_encabezado = columa_style()
    estilo_fila = fila_style()
    estilo_tabla = table_style_UMA()
    estilo_fila_moneda = fila_style_moneda()
    estilo_fila_moneda_total = fila_style_moneda_total()
    encabezados = []
    encabezados.append(Paragraph("No.", estilo_encabezado),)
    datos = sumar_ingresos_depto_diarios_urbanizacion(datos)
    for col in datos.columns:
        encabezados.append(Paragraph(col, estilo_encabezado),)
    filas = [encabezados]
    for index, item in datos.iterrows():
        if item["Fecha"] == "Total":
            estilo_moneda = estilo_fila_moneda_total
            estilo_fila_nombre = estilo_fila_moneda_total
            no = ""
        else:
            estilo_moneda = estilo_fila_moneda
            estilo_fila_nombre = estilo_fila
            no = str(int(index)+1)

        filas.append([
            Paragraph(no, estilo_fila),
            Paragraph(f'{item["Fecha"]}', estilo_fila_nombre),
            Paragraph(
                f'{item["Autorizaciones"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Licencias para Ejercer"]:,.2f}',
                      estilo_moneda),
            Paragraph(f'{item["Permisos de Construcción"]:,.2f}',
                      estilo_moneda),
            Paragraph(
                f'{item["Permisos de Construcción de Antenas"]:,.2f}', estilo_moneda),
            Paragraph(
                f'{item["Instlación de Rótulos"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Constancias"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Otros"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Total"]:,.2f}', estilo_moneda)
        ])

    tabla = Table(filas, colWidths=[
        30, 60,  70, 70, 70, 70, 70, 70, 70,  70])
    tabla.setStyle(estilo_tabla)
    return tabla


def tabla_ingreso_mensual_desarrollo_urbano(datos, ) -> Table:
    estilo_encabezado = columa_style()
    estilo_fila = fila_style()
    estilo_tabla = table_style_UMA()
    estilo_fila_moneda = fila_style_moneda()
    estilo_fila_moneda_total = fila_style_moneda_total()
    encabezados = []
    encabezados.append(Paragraph("No.", estilo_encabezado),)
    datos = sumar_ingresos_depto_mensual_urbanizacion(datos)
    for col in datos.columns:
        encabezados.append(Paragraph(col, estilo_encabezado),)
    filas = [encabezados]
    for index, item in datos.iterrows():
        if item["Mes"] == "Total":
            estilo_moneda = estilo_fila_moneda_total
            estilo_fila_nombre = estilo_fila_moneda_total
            no = ""
        else:
            estilo_moneda = estilo_fila_moneda
            estilo_fila_nombre = estilo_fila
            no = str(int(index)+1)

        filas.append([
            Paragraph(no, estilo_fila),
            Paragraph(f'{item["Mes"]}', estilo_fila_nombre),
            Paragraph(
                f'{item["Autorizaciones"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Licencias para Ejercer"]:,.2f}',
                      estilo_moneda),
            Paragraph(f'{item["Permisos de Construcción"]:,.2f}',
                      estilo_moneda),
            Paragraph(
                f'{item["Permisos de Construcción de Antenas"]:,.2f}', estilo_moneda),
            Paragraph(
                f'{item["Instlación de Rótulos"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Constancias"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Otros"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Total"]:,.2f}', estilo_moneda)
        ])

    tabla = Table(filas, colWidths=[
        30, 60,  70, 70, 70, 70, 70, 70, 70,  70])
    tabla.setStyle(estilo_tabla)
    return tabla


def tabla_ingreso_diario_admin_excel_urbanismo(excel, datos, ws):
    for index, item in datos.iterrows():
        ixd = index+1
        excel.fila_num += 1
        ws.append([
            ixd,
            item["Fecha"].strip(),
            f'{item["Autorizaciones"]:,.2f}',
            f'{item["Licencias para Ejercer"]:,.2f}',
            f'{item["Permisos de Construcción"]:,.2f}',
            f'{item["Permisos de Construcción de Antenas"]:,.2f}',
            f'{item["Instlación de Rótulos"]:,.2f}',
            f'{item["Constancias"]:,.2f}',
            f'{item["Otros"]:,.2f}',
            f'{item["Total"]:,.2f}',
        ])
    return ws
