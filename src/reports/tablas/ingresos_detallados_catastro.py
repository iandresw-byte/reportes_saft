from reportlab.platypus import Table, Paragraph
from src.reports.utils.manejador_data_frame import sumar_ingresos_departo_catastro
from src.reports.utils.manejador_data_depto_mensual import sumar_ingresos_depto_mensual_catastro
from src.reports.utils.manejador_data_depto_diario_frame import sumar_ingresos_depto_diarios_catastro
from src.ui.components.ui_style_table import columa_style, fila_style, fila_style_moneda, fila_style_moneda_total, table_style_UMA


def tabla_ingreso_detallado_catastro(datos, ) -> Table:
    estilo_encabezado = columa_style()
    estilo_fila = fila_style()
    estilo_tabla = table_style_UMA()
    estilo_fila_moneda = fila_style_moneda()
    estilo_fila_moneda_total = fila_style_moneda_total()
    encabezados = []
    encabezados.append(Paragraph("No.", estilo_encabezado),)
    datos = sumar_ingresos_departo_catastro(datos)
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
            Paragraph(f'{item["Venta de Dominio Pleno"]:,.2f}', estilo_moneda),
            Paragraph(
                f'{item["Servicio de Documentacion"]:,.2f}',  estilo_moneda),
            Paragraph(f'{item["Constancias"]:,.2f}',   estilo_moneda),
            Paragraph(
                f'{item["Servicio de Medidas y Remedidas"]:,.2f}', estilo_moneda),
            Paragraph(
                f'{item["Registros de Propiedad"]:,.2f}', estilo_moneda),
            Paragraph(
                f'{item["Venta de Lotes de Cementerio"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Inspecciones"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Otros"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Total Recibo"]:,.2f}', estilo_moneda)
        ])

    tabla = Table(filas, colWidths=[
        30, 40, 75, 160, 50, 50, 50, 50, 50, 50, 50, 50, 50])
    tabla.setStyle(estilo_tabla)
    return tabla


def tabla_ingreso_diario_catastro(datos, ) -> Table:
    estilo_encabezado = columa_style()
    estilo_fila = fila_style()
    estilo_tabla = table_style_UMA()
    estilo_fila_moneda = fila_style_moneda()
    estilo_fila_moneda_total = fila_style_moneda_total()
    encabezados = []
    encabezados.append(Paragraph("No.", estilo_encabezado),)
    datos = sumar_ingresos_depto_diarios_catastro(datos)
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
            Paragraph(f'{item["Venta de Dominio Pleno"]:,.2f}', estilo_moneda),
            Paragraph(
                f'{item["Servicio de Documentacion"]:,.2f}',  estilo_moneda),
            Paragraph(f'{item["Constancias"]:,.2f}',   estilo_moneda),
            Paragraph(
                f'{item["Servicio de Medidas y Remedidas"]:,.2f}', estilo_moneda),
            Paragraph(
                f'{item["Registros de Propiedad"]:,.2f}', estilo_moneda),
            Paragraph(
                f'{item["Venta de Lotes de Cementerio"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Inspecciones"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Otros"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Total"]:,.2f}', estilo_moneda)
        ])

    tabla = Table(filas, colWidths=[
        30, 60,  70, 70, 70, 70, 70, 70, 70, 70, 80])
    tabla.setStyle(estilo_tabla)
    return tabla


def tabla_ingreso_mensual_catastro(datos, ) -> Table:
    estilo_encabezado = columa_style()
    estilo_fila = fila_style()
    estilo_tabla = table_style_UMA()
    estilo_fila_moneda = fila_style_moneda()
    estilo_fila_moneda_total = fila_style_moneda_total()
    encabezados = []
    encabezados.append(Paragraph("No.", estilo_encabezado),)
    datos = sumar_ingresos_depto_mensual_catastro(datos)
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
            Paragraph(f'{item["Venta de Dominio Pleno"]:,.2f}', estilo_moneda),
            Paragraph(
                f'{item["Servicio de Documentacion"]:,.2f}',  estilo_moneda),
            Paragraph(f'{item["Constancias"]:,.2f}',   estilo_moneda),
            Paragraph(
                f'{item["Servicio de Medidas y Remedidas"]:,.2f}', estilo_moneda),
            Paragraph(
                f'{item["Registros de Propiedad"]:,.2f}', estilo_moneda),
            Paragraph(
                f'{item["Venta de Lotes de Cementerio"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Inspecciones"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Otros"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Total"]:,.2f}', estilo_moneda)
        ])

    tabla = Table(filas, colWidths=[
        30, 60,  70, 70, 70, 70, 70, 70, 70, 70, 80])
    tabla.setStyle(estilo_tabla)
    return tabla


def tabla_ingreso_diario_admin_excel_catastro(excel, datos, ws):
    for index, item in datos.iterrows():
        ixd = index+1
        excel.fila_num += 1
        ws.append([
            ixd,
            item["Fecha"].strip(),
            f'{item["Venta de Dominio Pleno"]:,.2f}',
            f'{item["Servicio de Documentacion"]:,.2f}',
            f'{item["Constancias"]:,.2f}',
            f'{item["Servicio de Medidas y Remedidas"]:,.2f}',
            f'{item["Registros de Propiedad"]:,.2f}',
            f'{item["Venta de Lotes de Cementerio"]:,.2f}',
            f'{item["Inspecciones"]:,.2f}',
            f'{item["Otros"]:,.2f}',
            f'{item["Total"]:,.2f}',
        ])
    return ws
