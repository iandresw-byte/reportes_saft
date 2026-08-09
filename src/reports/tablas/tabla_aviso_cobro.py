from reportlab.platypus import Table, Paragraph
from src.reports.utils.manejador_establecimientos import sumar_establecimientos_actividad
from src.ui.components.ui_style_table import columa_style, fila_style, fila_style_descripcion, fila_style_moneda, fila_style_moneda_total, table_estyle_aviso_gob_media_carta, table_style_UMA


ESTILO_ENCABEZADO_MORA = columa_style()
ESTILO_FILA_MORA = fila_style()
ESTILO_TABLA_MORA = table_estyle_aviso_gob_media_carta()
ESTILO_FILA_MONEDA_TOTAL = fila_style_moneda_total()


def tabla_aviso_mora_media_carta(datos) -> Table:



    encabezado = [
        Paragraph("No.", ESTILO_ENCABEZADO_MORA),
        Paragraph("Descripción", ESTILO_ENCABEZADO_MORA),
        Paragraph("Monto (L)", ESTILO_ENCABEZADO_MORA),
    ]

    filas_izq = [encabezado]
    filas_der = [encabezado]

    total = 0
    filas_num = len(datos)
    res = filas_num // 2

    for contador, item in enumerate(datos, start=1):

        monto = item["valor"] or 0
        total += monto

        fila = [
            item["cta_ingreso"] or "",
            item["nombre"] or "",
            f"{monto:,.2f}",
        ]

        if contador <= res + 1:
            filas_izq.append(fila)
        else:
            filas_der.append(fila)

    # Completar la columna derecha si la izquierda tiene una fila adicional
    if len(filas_izq) > len(filas_der) + 1:
        filas_der.append(["",  "**ULTIMA LINEA**", "", ]) # type: ignore

    # Total
    filas_der.append([
        "",
        "TOTAL",
        Paragraph(
            f"{total:,.2f}",
            ESTILO_FILA_MONEDA_TOTAL
        ),
    ])

    # Crear las dos tablas
    tabla_izq = Table(
        filas_izq,
        colWidths=[48, 172, 55]
    )
    tabla_izq.setStyle(ESTILO_TABLA_MORA)

    tabla_der = Table(
        filas_der,
        colWidths=[48, 172, 55]
    )
    tabla_der.setStyle(ESTILO_TABLA_MORA)

    # Tabla que contiene ambas
    tabla = Table(
        [[tabla_izq, tabla_der]],
        colWidths=[279, 279]
    )

    return tabla

def tabla_aviso_mora_media_carta_sami(datos) -> Table:
    estilo_encabezado = columa_style()
    estilo_fila = fila_style()
    estilo_fila_desc = fila_style_descripcion()
    estilo_tabla = table_estyle_aviso_gob_media_carta()
    estilo_fila_moneda = fila_style_moneda()
    estilo_fila_moneda_total = fila_style_moneda_total()


    filas_izq = [[Paragraph("No.", estilo_encabezado), Paragraph("Descripción", estilo_encabezado), Paragraph("Monto (L)", estilo_encabezado)]]
    filas_der = [[Paragraph("No.", estilo_encabezado), Paragraph("Descripción", estilo_encabezado), Paragraph("Monto (L)", estilo_encabezado)]]
            
    total = 0
    filas_num = len(datos)
    res = int(filas_num/2)
    contador=0

    for  item in datos:
        monto = item["valor"] or 0
        contador+=1
        if contador<=res+1:
            filas_izq.append(
                [
                    Paragraph(item["cta_ingreso"],estilo_fila), 
                    Paragraph(item["nombre"],estilo_fila_desc), 
                    Paragraph(f"{monto:,.2f}", estilo_fila_moneda)
                    
                    ])
            total += monto
        else:
            filas_der.append(
                [
                    Paragraph(item["cta_ingreso"],estilo_fila), 
                    Paragraph(item["nombre"],estilo_fila_desc), 
                    Paragraph(f"{monto:,.2f}", estilo_fila_moneda)
                    
                    ])
            total += monto

    
    if len(filas_izq) > len(filas_der)+1:
                filas_der.append([
                Paragraph("",estilo_fila),
                Paragraph("**ULTIMA LINEA**", estilo_fila),
                Paragraph(f"",estilo_fila),])
    
    filas_der.append([
                Paragraph("",estilo_fila),
                Paragraph("TOTAL", estilo_fila),
                Paragraph(f"{total:,.2f}",estilo_fila_moneda_total),])
    
    tabla_der = Table(filas_der, colWidths=[50,172, 55])
    tabla_der.setStyle(estilo_tabla)
    tabla_izq = Table(filas_izq, colWidths=[50,172, 55])
    tabla_izq.setStyle(estilo_tabla)

    fila_group = [tabla_izq, tabla_der]
    tabla = Table(
        [fila_group],
        colWidths=[ 280, 280],
    )


    return tabla

def tabla_aviso_carta(datos) -> Table:
    estilo_encabezado = columa_style()
    estilo_fila = fila_style()
    estilo_fila_desc = fila_style_descripcion()
    estilo_tabla = table_estyle_aviso_gob_media_carta()
    estilo_fila_moneda = fila_style_moneda()
    estilo_fila_moneda_total = fila_style_moneda_total()


    filas_izq = [[Paragraph("No.", estilo_encabezado), Paragraph("Descripción", estilo_encabezado), Paragraph("Monto (L)", estilo_encabezado)]]
    filas_der = [[Paragraph("No.", estilo_encabezado), Paragraph("Descripción", estilo_encabezado), Paragraph("Monto (L)", estilo_encabezado)]]
            
    total = 0
    filas_num = len(datos)
    res = int(filas_num/2)
    contador=0

    for  item in datos:
        monto = item["valor"] or 0
        contador+=1
        if contador<=res+1:
            filas_izq.append(
                [
                    Paragraph(item["cta_ingreso"],estilo_fila), 
                    Paragraph(item["nombre"],estilo_fila_desc), 
                    Paragraph(f"{monto:,.2f}", estilo_fila_moneda)
                    
                    ])
            total += monto
        else:
            filas_der.append(
                [
                    Paragraph(item["cta_ingreso"],estilo_fila), 
                    Paragraph(item["nombre"],estilo_fila_desc), 
                    Paragraph(f"{monto:,.2f}", estilo_fila_moneda)
                    
                    ])
            total += monto

    
    if len(filas_izq) > len(filas_der)+1:
                filas_der.append([
                Paragraph("",estilo_fila),
                Paragraph("**ULTIMA LINEA**", estilo_fila),
                Paragraph(f"",estilo_fila),])
    
    filas_der.append([
                Paragraph("",estilo_fila),
                Paragraph("TOTAL", estilo_fila),
                Paragraph(f"{total:,.2f}",estilo_fila_moneda_total),])
    
    tabla_der = Table(filas_der, colWidths=[48, 172, 55])
    tabla_der.setStyle(estilo_tabla)
    tabla_izq = Table(filas_izq, colWidths=[48, 172, 55])
    tabla_izq.setStyle(estilo_tabla)

    fila_group = [tabla_izq, tabla_der]
    tabla = Table(
        [fila_group],
        colWidths=[ 279, 279],
    )


    return tabla