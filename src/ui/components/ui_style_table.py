from reportlab.platypus import TableStyle
from reportlab.lib.styles import StyleSheet1
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle

color_colum_name =colors.HexColor("#4F81BD")
def table_style():
    return TableStyle(
        [
            # Encabezado
            ("BACKGROUND", (0, 0), (-1, 0), color_colum_name),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

            # Bordes y fondo general
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

            # 🔹 Alineaciones personalizadas por columna
            # Primera a la izquierda
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            # Segunda columna en el centro
            ("ALIGN", (1, 0), (1, -1), "CENTER"),
            # Tercera columna en el centro
            ("ALIGN", (2, 0), (2, -1), "CENTER"),
            # Cuarta columna en el centro
            ("ALIGN", (3, 0), (3, -1), "CENTER"),
            # Quinta columna en el centro
            ("ALIGN", (4, 0), (4, -1), "CENTER"),
        ]
    )

def table_style_UMA():
    return TableStyle(
        [
            # Encabezado
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.red),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

            # Bordes y fondo general
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

            # Primera columna izquierda
            ("ALIGN", (0, 0), (0, -1), "LEFT"),

            # Desde columna 4 hasta la última alineadas a la derecha
            ("ALIGN", (4, 1), (8, -1), "RIGHT"),
        ]
    )

def table_estyle_aviso():
    return TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ALIGN", (2, 1), (2, -1), "RIGHT"),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ])

def table_estyle_aviso_gob_media_carta():
    return TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 7),
                ("ALIGN", (2, 1), (2, -1), "RIGHT"),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ])

def table_estyle_aviso_gob_carta():
    return TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), color_colum_name),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (2, 1), (2, -1), "RIGHT"),
            ])

def columa_style():
    return ParagraphStyle(
        name="TablaColumnas",
        textColor=colors.white,
        fontName="Helvetica",
        fontSize=8,
        leading=10,   # espacio entre líneas
        alignment=1,  # 0=izq, 1=centro, 2=derecha
    )

def frima_estilo():
    return ParagraphStyle(
        name='Firma',
        fontSize=11,
        fontName="Century-Gothic",
        alignment=1,  # justificado
    )

def frima_estilo_aviso():
    return ParagraphStyle(
        name='Firma',
        fontSize=7,
        fontName="Century-Gothic",
        alignment=1,  # justificado
    )

def fila_style():
    return ParagraphStyle(
        name="FilaColumnas",
        textColor=colors.black,
        fontName="Helvetica",
        fontSize=8,
        leading=10,   # espacio entre líneas
        alignment=1,  # 0=izq, 1=centro, 2=derecha
    )

def fila_style_descripcion():
    return ParagraphStyle(
        name="FilaColumnas",
        textColor=colors.black,
        fontName="Helvetica",
        fontSize=8,
        leading=10,   # espacio entre líneas
        alignment=0,  # 0=izq, 1=centro, 2=derecha
    )

def fila_style_moneda():
    return ParagraphStyle(
        name="FilaColumnasMoneda",
        textColor=colors.black,
        fontName="Helvetica",
        fontSize=8,
        leading=10,   # espacio entre líneas
        alignment=2,  # 0=izq, 1=centro, 2=derecha
    )

def fila_style_moneda_total():
    return ParagraphStyle(
        name="FilaColumnasMonedaTotal",
        textColor=colors.black,
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,   # espacio entre líneas
        alignment=2,  # 0=izq, 1=centro, 2=derecha
    )

def estilos_licencia_uma():
    estilos = StyleSheet1()
    estilos.add(ParagraphStyle(
        name='TituloMuni',
        fontSize=25,
        alignment=1,  # centrado
        leading=20,
        spaceAfter=10,
        fontName="SourceSansPro-Bold"
    ))
    estilos.add(ParagraphStyle(
        name='TituloDepto',
        fontSize=25,
        alignment=1,  # centrado
        leading=20,
        spaceAfter=10,
        fontName="SourceSansPro-Bold"
    ))
    estilos.add(ParagraphStyle(
        name='Titulo',
        fontSize=28,
        alignment=1,  # centrado
        leading=20,
        textColor="#008000",
        spaceAfter=10,
        fontName="SourceSansPro-Bold"
    ))
    estilos.add(ParagraphStyle(
        name='Telefono',
        fontSize=15,
        alignment=1,  # centrado
        leading=10,
        spaceAfter=10,
        fontName="SourceSansPro"
    ))
    estilos.add(ParagraphStyle(
        name='NumPermiso',
        fontSize=20,
        textColor="#008000",
        fontName="GOTHICB",
        # backColor=colors.whitesmoke,  # Fondo gris claro
        leftIndent=8,
        borderWidth=500,
        rightIndent=8,
        leading=15,
        alignment=2
    ))
    estilos.add(ParagraphStyle(
        name='labels',
        fontSize=12,
        textColor="#1d444d",
        fontName="SourceSansPro-Bold",
        # backColor=colors.whitesmoke,  # Fondo gris claro
        leftIndent=3,
        borderWidth=500,
        rightIndent=3,
        leading=15,
        alignment=1
    ))
    estilos.add(ParagraphStyle(
        name='labels_data',
        fontSize=15,
        textColor="#1d444d",
        fontName="SourceSansPro-Bold",
        # backColor=colors.whitesmoke,  # Fondo gris claro
        leftIndent=8,
        borderWidth=500,
        rightIndent=8,
        leading=15,
        alignment=0
    ))
    estilos.add(ParagraphStyle(
        name='Valor',
        fontSize=13,
        textColor="#000000",
        fontName="SourceSansPro-Bold",
        # backColor=colors.whitesmoke,  # Fondo gris claro
        leftIndent=1,
        borderWidth=500,
        rightIndent=1,
        leading=15,
        alignment=1
    ))
    return estilos

def estilos_parrafo():
    estilos = StyleSheet1()
    estilos.add(ParagraphStyle(
        name='TituloMuni',
        fontSize=36,
        alignment=1,  # centrado
        leading=35,
        spaceAfter=10,
        fontName="Malgun-Bold"
    ))
    estilos.add(ParagraphStyle(
        name='TituloPrincipal',
        fontSize=20,
        textColor=colors.black,
        alignment=1,  # centrado
        fontName="Jhenghei",
        spaceAfter=15
    ))
    estilos.add(ParagraphStyle(
        name='TituloMuniMedia',
        fontSize=13,
        alignment=1,  # centrado
        #leading=35,
        spaceAfter=1,
        fontName="Malgun-Bold"
    ))
    estilos.add(ParagraphStyle(
        name='TituloPrincipalMedia',
        fontSize=20,
        textColor=colors.black,
        alignment=1,  # centrado
        fontName="Jhenghei",
        spaceAfter=2
    ))
    estilos.add(ParagraphStyle(
        name='Label',
        fontSize=11,
        textColor=colors.green,
        fontName="GOTHICB",
        leading=15,
        spaceBefore=6
    ))
    estilos.add(ParagraphStyle(
        name='Valor',
        fontSize=11,
        textColor=colors.black,
        fontName="GOTHICB",
        backColor=colors.whitesmoke,  # Fondo gris claro
        leftIndent=8,
        borderWidth=50,
        rightIndent=8,
        leading=15,
        alignment=1
    ))
    estilos.add(ParagraphStyle(
        name='NumPermiso',
        fontSize=20,
        textColor="#008000",
        fontName="GOTHICB",
        # backColor=colors.whitesmoke,  # Fondo gris claro
        leftIndent=8,
        borderWidth=500,
        rightIndent=8,
        leading=15,
        alignment=1
    ))
    estilos.add(ParagraphStyle(
        name='Texto',
        fontSize=11,
        textColor=colors.black,
        fontName="Century-Gothic",
        leading=15,
        alignment=4,  # justificado
        spaceBefore=10,
        spaceAfter=10
    ))
    estilos.add(ParagraphStyle(
        name='Firma',
        fontSize=11,
        fontName="Century-Gothic",
        alignment=1,  # justificado
    ))
    estilos.add(ParagraphStyle(
        name='parrafo',
        fontSize=11,
        textColor=colors.black,
        fontName="Century-Gothic",
        leading=15,
        alignment=4,  # justificado
        spaceBefore=5,
        spaceAfter=5
    ))
    estilos.add(ParagraphStyle(
        name='la_esperanza_title',
        fontSize=12,
        textColor=colors.black,
        fontName="AHARONI-BOLD",
        leading=15,
        alignment=1,  # justificado
        spaceBefore=0,
        spaceAfter=0
    ))
    estilos.add(ParagraphStyle(
        name='la_esperanza_campos',
        fontSize=9,
        textColor=colors.black,
        fontName="Arial-Rounded-MT-Bold",
        leading=15,
        alignment=0,  # justificado
        spaceBefore=5,
        spaceAfter=5
    ))
    estilos.add(ParagraphStyle(
        name='la_esperanza_telefono',
        fontSize=9,
        textColor="#153D63",
        fontName="ABADI-BOLD",
        leading=15,
        alignment=1,  # justificado
        spaceBefore=2,
        spaceAfter=5
    ))
    estilos.add(ParagraphStyle(
        name='la_esperanza_title_ope',
        fontSize=23.2,
        textColor="#0F4761",
        fontName="AMASIS-BOLD",
        leading=10,
        alignment=1,  # justificado
        spaceBefore=5,
        spaceAfter=5
    ))
    estilos.add(ParagraphStyle(
        name='la_esperanza_num_ope',
        fontSize=28,
        textColor="#EE0000",
        fontName="Britannic-Bold",
        leading=20,
        alignment=2,  # justificado
        spaceBefore=0,
        spaceAfter=10,
        rightIndent=20
    ))
    estilos.add(ParagraphStyle(
        name='la_esperanza_parrafo',
        fontSize=10,
        textColor=colors.black,
        fontName="ABADI",
        leading=10,
        alignment=0,  # justificado
        spaceBefore=0,
        spaceAfter=10
    ))
    estilos.add(ParagraphStyle(
        name='la_esperanza_campos_firma',
        fontSize=9,
        textColor=colors.black,
        fontName="ABADI-BOLD",
        leading=0,
        alignment=1,  # justificado
        spaceBefore=5,
        spaceAfter=10
    ))
    estilos.add(ParagraphStyle(
        name='la_esperanza_firma_alc',
        fontSize=9,
        textColor=colors.white,
        fontName="ABADI-BOLD",
        leading=0,
        alignment=1,  # justificado
        spaceBefore=5,
        spaceAfter=10
    ))
    estilos.add(ParagraphStyle(
        name='horario',
        fontSize=6,
        textColor=colors.red,
        fontName="Times-Roman",
        leading=0,
        alignment=1,  # justificado
        spaceBefore=5,
        spaceAfter=5
    ))
    estilos.add(ParagraphStyle(
        name='horario_title',
        fontSize=6,
        underlineColor=colors.red,
        underlineWidth=0.5,
        underlineGap=0.5,
        textColor=colors.red,
        underline=True,
        fontName="Times-Roman",
        leading=0,
        alignment=1,  # justificado
        spaceBefore=0,
        spaceAfter=0
    ))

    estilos.add(ParagraphStyle(
        name='concepcion_telefono',
        fontSize=11,
        textColor="#0563C1",
        fontName="Helvetica",
        leading=13,
        alignment=1,  # centradp
        spaceBefore=5,
        spaceAfter=25
    ))
    estilos.add(ParagraphStyle(
        name='concepcion_title_ope',
        fontSize=24,
        textColor=colors.black,
        fontName="Helvetica",
        leading=26,
        alignment=1,  # centrado
        spaceBefore=5,
        spaceAfter=5
    ))

    estilos.add(ParagraphStyle(
        name='concepcion_parrafo',
        fontSize=14,
        textColor=colors.black,
        fontName="Helvetica",
        leading=16,
        alignment=0,  # izquierda
        spaceBefore=5,
        spaceAfter=5
    ))

    estilos.add(ParagraphStyle(
        name='concepcion_campos_firma',
        fontSize=14,
        textColor=colors.black,
        fontName="Helvetica-Bold",
        leading=14,
        alignment=1,  # centrado
        spaceBefore=0,
        spaceAfter=0
    ))
    estilos.add(ParagraphStyle(
        name='concepcion_title',
        fontSize=28,
        textColor=colors.black,
        fontName="Helvetica-Bold",
        leading=30,
        alignment=1,  # centrado
        spaceBefore=5,
        spaceAfter=5
    ))
    estilos.add(ParagraphStyle(
        name='concepcion_campos',
        fontSize=14,
        textColor=colors.black,
        fontName="Helvetica",
        leading=16,
        alignment=0,  # izquierda
        spaceBefore=0,
        spaceAfter=5
    ))
    estilos.add(ParagraphStyle(
        name='concepcion_num_ope',
        fontSize=12,
        textColor=colors.black,
        fontName="Helvetica-Bold",
        leading=20,
        alignment=0,  # justificado
        spaceBefore=0,
        spaceAfter=10
    ))
    estilos.add(ParagraphStyle(
                name="firma_apremio",
                alignment=1,
                fontSize=10
                ))
    return estilos

def table_per_ope():
    return TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        # Fondo gris para valores
        ("BACKGROUND", (0, 1), (0, -1), colors.whitesmoke),
        ("BACKGROUND", (1, 1), (1, -1), colors.transparent),
        ("BACKGROUND", (2, 1), (2, -1), colors.whitesmoke),
        ("BACKGROUND", (3, 1), (3, -1), colors.transparent),
        ("BACKGROUND", (4, 1), (4, -1), colors.whitesmoke),
    ])

def table_per_ope_2():
    return TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        # Fondo gris para valores
        ("BACKGROUND", (0, 1), (0, -1), colors.whitesmoke),
        ("BACKGROUND", (1, 1), (1, -1), colors.transparent),
        ("BACKGROUND", (2, 1), (2, -1), colors.whitesmoke),
    ])

def table_fecha_lateral():
    return TableStyle([
        # Fondo general

        # Texto
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        # Centrar horizontal
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        # Centrar vertical
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # Padding
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        # Quitar bordes
        # ('BOX', (0, 0), (-1, -1), 0, colors.white),
        # ('GRID', (0, 0), (-1, -1), 0, colors.white),
        # SOLO línea entre filas
        ('LINEBELOW', (0, 1), (-1, 1), 1, colors.gray),
        ('LINEBELOW', (0, 3), (-1, 3), 1, colors.gray),
        ('LINEBELOW', (0, 5), (-1, 5), 1, colors.gray),
        ('LINEBELOW', (0, 7), (-1, 7), 1, colors.gray)

    ])
