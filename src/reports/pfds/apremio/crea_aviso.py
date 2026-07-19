
from src.ui.components.ui_style_table import columa_style, estilos_parrafo, fila_style, fila_style_moneda
from src.ui.components.ui_style_pdf import getSampleStyleSheet as estilos_mod
from reportlab.platypus import  Table, TableStyle, Paragraph
from datetime import date
def crear_aviso(self, contribuyente, tipo):
    estilos = estilos_mod()
    elementos = []

    if tipo == "ORIGINAL":
        titulo = "ORIGINAL"
    else:
        titulo = "COPIA"
    hoy = date.today()
    periodo = Paragraph(f"<b>Periodo:</b> {contribuyente['periodo']}", estilos["Normal"],  )
    nombre = Paragraph( f"<b>Contribuyente:</b> {contribuyente['nombre']}",  estilos["Normal"],)
    dni = Paragraph( f"<b>DNI:</b> {contribuyente['dni']}", estilos["Normal"], )
    direccion = Paragraph(f"<b>Dirección:</b> {contribuyente['direccion']}", estilos["Normal"],)
    clave_cata = Paragraph( f"<b>Claves Catastrales:</b> {contribuyente['clave_catastro']}", estilos["Normal"],)
    num_documento = Paragraph(f"<b>No. RDP-{hoy.year}-{contribuyente['num_documeto']}</b>",estilos["Normal_rojo_bold"],)

    fila = [nombre, dni, periodo,  num_documento]
    fila_2 = [direccion,   clave_cata, Paragraph("",), Paragraph("",),]

    tabla_datos_generales = Table(
        [fila, fila_2],
        colWidths=[270, 100, 140,90],  # ajusta según tus márgenes
    )
    tabla_datos_generales.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "RIGHT"),
        ('SPAN', (1, 1), (3, 1)),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))

    elementos.append(tabla_datos_generales)
    
    return elementos

def crear_aviso_original(self, contribuyente, tipo):
    estilos = estilos_mod()
    elementos = []

    if tipo == "ORIGINAL":
        titulo = "ORIGINAL"
    else:
        titulo = "COPIA"
    hoy = date.today()
    periodo = Paragraph(f"<b>Periodo:</b> {contribuyente['periodo']}", estilos["Normal"],  )
    nombre = Paragraph( f"<b>Contribuyente:</b> {contribuyente['nombre']}",  estilos["Normal"],)
    dni = Paragraph( f"<b>DNI:</b> {contribuyente['dni']}", estilos["Normal"], )
    direccion = Paragraph(f"<b>Dirección:</b> {contribuyente['direccion']}", estilos["Normal"],)
    clave_cata = Paragraph( f"<b>Claves Catastrales:</b> {contribuyente['clave_catastro']}", estilos["Normal"],)
    num_documento = Paragraph(f"<b>No. RDP-{hoy.year}-{contribuyente['num_documeto']}</b>",estilos["Normal_rojo_bold"],)

    fila = [nombre, dni, periodo,  num_documento]
    fila_2 = [direccion,   clave_cata, Paragraph("",), Paragraph("",),]

    tabla_datos_generales = Table(
        [fila, fila_2],
        colWidths=[220, 100, 140,90],  # ajusta según tus márgenes
    )
    tabla_datos_generales.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "RIGHT"),
        ('SPAN', (1, 1), (3, 1)),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))

    elementos.append(tabla_datos_generales)
    
    return elementos


def crear_aviso_carta(self, contribuyente, tipo):
    estilos = estilos_mod()
    elementos = []

    if tipo == "ORIGINAL":
        titulo = "ORIGINAL"
    else:
        titulo = "COPIA"
    hoy = date.today()
    periodo = Paragraph(f"<b>Periodo:</b> {contribuyente['periodo']}", estilos["Normal_10"],  )
    nombre = Paragraph( f"<b>Contribuyente:</b> {contribuyente['nombre']}",  estilos["Normal_10"],)
    dni = Paragraph( f"<b>DNI:</b> {contribuyente['dni']}", estilos["Normal_10"], )
    direccion = Paragraph(f"<b>Dirección:</b> {contribuyente['direccion']}", estilos["Normal_10"],)
    clave_cata = Paragraph( f"<b>Claves Catastrales:</b> {contribuyente['clave_catastro']}", estilos["Normal_10"],)
    num_documento = Paragraph(f"<b>No. RDP-{hoy.year}-{contribuyente['num_documeto']}</b>",estilos["Normal_rojo_bold_10"],)

    fila = [nombre,  "",  "",  num_documento]
    fila_2 = [dni,  "",    periodo, ""]
    fila_3 = [direccion,   "", "", ""]
    fila_4 = [clave_cata, "" ,  "", ""]

    tabla_datos_generales = Table(
        [fila, fila_2, fila_3, fila_4],
        colWidths=[220, 100, 140,100],  # ajusta según tus márgenes
    )
    tabla_datos_generales.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "RIGHT"),
          ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

    # Fila 0: unir columnas 1 y 2
    ('SPAN', (0, 0), (2, 0)),

    # Fila 1: unir columnas 1 y 3
    ('SPAN', (0, 1), (1, 1)),
    ('SPAN', (2, 1), (3, 1)),

    # Fila 2: unir columnas 1 y 3
    ('SPAN', (0, 2), (3, 2)),

    # Fila 3: unir columnas 1 y 3
    ('SPAN', (0, 3), (3, 3)),

    ("TOPPADDING", (0, 0), (-1, -1), 2),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))

    elementos.append(tabla_datos_generales)
    
    return elementos