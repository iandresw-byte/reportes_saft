from reportlab.platypus import Table, Paragraph
from src.reports.utils.manejador_establecimientos import sumar_establecimientos_actividad
from src.ui.components.ui_style_table import columa_style, fila_style, fila_style_moneda, fila_style_moneda_total, table_style_UMA


def tabla_establecimietos_x_actividad_pdf(datos) -> Table:
    estilo_encabezado = columa_style()
    estilo_fila = fila_style()
    estilo_tabla = table_style_UMA()
    estilo_fila_moneda = fila_style_moneda()
    estilo_fila_moneda_total = fila_style_moneda_total()
    encabezados = []
    datos = sumar_establecimientos_actividad(datos, tipo_rpt="pdf")
    encabezados.append(Paragraph("No.", estilo_encabezado),)
    for col in datos.columns:
        encabezados.append(Paragraph(col, estilo_encabezado),)
    filas = [encabezados]
    for index, item in datos.iterrows():
        dni = item["Registro Tributario Municipal (RTM)"].strip()

        if item["Nombre Establecimiento"] == "":
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
            Paragraph(f'{item["Nombre Establecimiento"]}', estilo_fila_nombre),
            Paragraph(f'{item["Comerciante"]}', estilo_fila_nombre),
            Paragraph(f'{item["Cuenta Actividad Economica"]}', estilo_fila_nombre),
            Paragraph(f'{item["Direccion Establecimiento"]}', estilo_fila_nombre),
            Paragraph(f'{item["Telefono"]}', estilo_fila_nombre),
            Paragraph(f'{item["Impuesto Año Actual"]:,.2f}', estilo_moneda),
            Paragraph(f'{item["Impuesto Años Anteriores"]:,.2f}',  estilo_moneda),
            Paragraph(f'{item["Otros Saldos"]:,.2f}',  estilo_moneda),
            Paragraph(f'{item["TOTAL"]:,.2f}', estilo_moneda),
        ])
   
    tabla = Table(filas, colWidths=[
            25, 85, 110, 110, 60, 150, 50, 45, 45,45,50])
    
    tabla.setStyle(estilo_tabla)
    return tabla


def tabla_establecimietos_x_actividad_excel(excel, datos, ws):
    for index, item in datos.iterrows():
        ixd = index+1
        excel.fila_num += 1
        ws.append([
            ixd,
            item["Registro Tributario Municipal (RTM)"].strip(),
            item["Establecimiento"].strip(),
            item["DNI"],
            item["Comerciante"].strip(),
            item["Cuenta Actividad Economica"].strip(),
            item["Direccion"].strip(),
            item["Telefono"].strip(),
            item["Inicio Saldos"].strip(),
            item["Facturado Hasta"].strip(),
            f'{item["Saldo Año Actual Industria"]:,.2f}',
            f'{item["Saldo Año Actual Comercio"]:,.2f}',
            f'{item["Saldo Año Actual Servicio"]:,.2f}',
            f'{item["Saldo Años Anteriores Industria"]:,.2f}',
            f'{item["Saldo Años Anteriores Comercio"]:,.2f}',
            f'{item["Saldo Años Anteriores Servicio"]:,.2f}',
            f'{item["Saldos Permiso de Operacion"]:,.2f}',
            f'{item["Intereses"]:,.2f}',
            f'{item["Recargos"]:,.2f}',
            f'{item["Multas"]:,.2f}',
            f'{item["Descuentos"]:,.2f}',
            f'{item["Otros Saldos"]:,.2f}',
            f'{item["Total"]:,.2f}',
        ])
    return ws
