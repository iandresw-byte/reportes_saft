from reportlab.platypus import Table, Paragraph

from src.ui.components.ui_style_table import estilos_licencia_uma, table_fecha_lateral


def tabla_licencia_ambienntal(datos, iconos) -> Table:

    fila = estilos_licencia_uma()

    estilos_tabla_fecha = table_fecha_lateral()
    fila_icon_labels = []

    labels = [Paragraph("NOMBRE DEL PROPIETARIO:", fila["labels_data"]),
              Paragraph("IDENTIDAD:", fila["labels_data"]),
              Paragraph("ES PROPIETARIA DE:", fila["labels_data"]),
              Paragraph("UBICADA EN:", fila["labels_data"]),
              Paragraph("FECHA SOLICITUD", fila["labels"]),
              Paragraph("FECHA VENCE", fila["labels"]),
              Paragraph("No. RECIBO", fila["labels"]),
              Paragraph("PERIODO FISCAL", fila["labels"])]

    for i, label in enumerate(labels):
        data = [[iconos[i], label]]
        ancho = [25, 350]
        if i > 3:
            ancho = [25, 130]
        tabla = [Table(data, colWidths=ancho)]
        fila_icon_labels.append(tabla)

    valor = [[Paragraph(f"{datos["propietario"]}", fila["Valor"])],  # 0
             [Paragraph(f"{datos["dni"]}", fila["Valor"])],  # 1
             [Paragraph(f"{datos["establecimiento"]}", fila["Valor"])],  # 2
             [Paragraph(f"{datos["direccion_establecimento"]}",
                        fila["Valor"])],  # 3
             [Paragraph(f"{datos["fecha_solicitud"]}", fila["Valor"])],  # 4
             [Paragraph(f"{datos["fecha_vence"]}", fila["Valor"])],  # 5
             [Paragraph(f"{datos["num_recibo"]}", fila["Valor"])],  # 6
             [Paragraph(f"{datos["periodo"]}", fila["Valor"])]]  # 7
    tabla_propitario = Table(
        [fila_icon_labels[0], valor[0],
         fila_icon_labels[1], valor[1],
         fila_icon_labels[2], valor[2],
         fila_icon_labels[3], valor[3]],
        colWidths=[340],  # ajusta según tus márgenes
    )
    tabla_propitario.setStyle(estilos_tabla_fecha)
    tabla_fechas = Table(
        [fila_icon_labels[6], valor[6],
         fila_icon_labels[4], valor[4],
         fila_icon_labels[5], valor[5],
         fila_icon_labels[7], valor[7]],
        colWidths=[140]
    )
    tabla_fechas.setStyle(estilos_tabla_fecha)

    fila = [tabla_propitario, "", tabla_fechas]
    tabla_data = Table(
        [fila],
        colWidths=[340, 40, 140],  # ajusta según tus márgenes
    )
    return tabla_data
