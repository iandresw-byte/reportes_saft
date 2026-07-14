from reportlab.platypus import Table, Paragraph
from src.reports.utils.manejador_abonados_sp import sumar_mora_abonados_servicios
from src.ui.components.ui_style_table import columa_style, fila_style, fila_style_moneda, fila_style_moneda_total, table_style_UMA


def tabla_abonados_servicio(datos, tipo_cta=0) -> Table:
    estilo_encabezado = columa_style()
    estilo_fila = fila_style()
    estilo_tabla = table_style_UMA()
    estilo_fila_moneda = fila_style_moneda()
    estilo_fila_moneda_total = fila_style_moneda_total()
    encabezados = []
    encabezados.append(Paragraph("No.", estilo_encabezado),)
    encabezados.append(Paragraph("DNI.", estilo_encabezado),)
    encabezados.append(Paragraph("Nombre Abonado.", estilo_encabezado),)
    encabezados.append(Paragraph("Codigo", estilo_encabezado),)
    encabezados.append(Paragraph("Cuenta Abonado", estilo_encabezado),)
    encabezados.append(Paragraph("Cuenta Servicio", estilo_encabezado),)
    encabezados.append(Paragraph("Nombe Servicio", estilo_encabezado),)
    encabezados.append(Paragraph("Inicio Mora", estilo_encabezado),)
    encabezados.append(Paragraph("Fin Mora", estilo_encabezado),)
    encabezados.append(Paragraph("Mora Actual", estilo_encabezado),)
    encabezados.append(Paragraph("Mora Años Ant.", estilo_encabezado),)
    encabezados.append(Paragraph("Intereses", estilo_encabezado),)
    encabezados.append(Paragraph("Recargos", estilo_encabezado),)
    encabezados.append(Paragraph("TOTAL", estilo_encabezado),)
    datos = sumar_mora_abonados_servicios(datos)
    
    filas = [encabezados]
    for index, item in datos.iterrows():
        dni = item["DNI"].strip()

        if item["Anio Fin Mora"] == "Total":
            estilo_moneda = estilo_fila_moneda_total
            estilo_fila_nombre = estilo_fila_moneda_total
            no = ""
        else:
            estilo_moneda = estilo_fila_moneda
            estilo_fila_nombre = estilo_fila
            no = str(int(index)+1)
  
        filas.append([
            Paragraph(no, estilo_fila),
            Paragraph(dni, estilo_fila),
            Paragraph(f'{item["Nombre Completo"]}', estilo_fila_nombre),
            Paragraph(f'{item["Codigo"]}', estilo_fila_nombre),
            Paragraph(f'{item["Cuenta"]}', estilo_fila_nombre),
            Paragraph(f'{item["Cuenta Ingreso"]}', estilo_fila_nombre),
            Paragraph(f'{item["Nombre Servicio"]}', estilo_fila_nombre),
            Paragraph(f'{item["Mes Incio Mora"]}-{item["Anio Inicio Mora"]}', estilo_fila_nombre),
            Paragraph(f'{item["Mes Fin Mora"]}-{item["Anio Fin Mora"]}', estilo_fila_nombre),
            Paragraph(f'{item["Mora Año Actual"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Mora Años Anteriores"]:,.2f}',  estilo_moneda),
            Paragraph(f'{item["Intereses"]:,.2f}',  estilo_moneda),
            Paragraph(f'{item["Recargos"]:,.2f}',  estilo_moneda),
            Paragraph(f'{item["TOTAL"]:,.2f}', estilo_moneda),
        ])
   
    tabla = Table(filas, colWidths=[
            25, 50, 110, 45, 45, 50, 110, 60, 60,45,45,45,45,45])
    
    tabla.setStyle(estilo_tabla)
    return tabla


def tabla_abonados_servicio_excel(excel, datos, ws):
    for index, item in datos.iterrows():
        ixd = index+1
        excel.fila_num += 1
        ws.append([
            ixd,
            item["DNI"].strip(),
            item["Nombre Completo"].strip(),
            item["Codigo"],
            item["Cuenta"].strip(),
            item["Cuenta Ingreso"].strip(),
            item["Nombre Servicio"].strip(),
            item["Mes Incio Mora"].strip(),
            item["Anio Inicio Mora"],
            item["Mes Fin Mora"].strip(),
            item["Anio Fin Mora"],
            f'{item["Mora Año Actual"]:,.2f}',
            f'{item["Mora Años Anteriores"]:,.2f}',
            f'{item["Intereses"]:,.2f}',
            f'{item["Recargos"]:,.2f}',
            f'{item["TOTAL"]:,.2f}',
        ])
    return ws
