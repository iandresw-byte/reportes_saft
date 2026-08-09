from flet import Container, CrossAxisAlignment, Radio, TextStyle, RadioGroup, LabelPosition, Column,  MainAxisAlignment, Row, Ref
from src.ui.components.ui_colors import color_check, color_texto


def create_radio(value='0', label_text="") -> Radio:
    return Radio(value=value,
                 label=label_text,
                 fill_color=color_check(),
                 label_style=TextStyle(
                     size=10, color=color_texto(), font_family="Tahoma")
                 )


def rd_tipo_factura(tipo_impuesto, mostrar_todos=True) -> RadioGroup:

    opciones = [
        create_radio(value="0", label_text="Otras Tasas"),
        create_radio(value="1", label_text="Bienes Inmuebles"),
        create_radio(value="4", label_text="Impuesto Personal"),
        create_radio(value="2,3", label_text="Industria, Comercio y Servicio"),
        create_radio(value="8", label_text="Abonos a Facturas"),

    ]

    # Agregar la última opción solo si se necesita
    if mostrar_todos:
        opciones.append(
            create_radio(
                value="5",
                label_text="Servicios Públicos"
            )
        )
        opciones.append(
            create_radio(
                value="7",
                label_text="Planes de Pago"
            )
        )
        opciones.append(
            create_radio(
                value="0,1,2,3,4,5,7",
                label_text="Todos (General)"
            )
        )

    return RadioGroup(
        ref=tipo_impuesto,
        value="0,1,2,3,4,5,7" if mostrar_todos else "0",
        content=Column(opciones)
    )


def rd_estratificacion(tamano_estatificacion):
    return RadioGroup(
        ref=tamano_estatificacion,
        value="%",
        content=Column([
            create_radio(value="0", label_text="Microempresas"),
            create_radio(value="1", label_text="Pequeña Empresa"),
            create_radio(value="2", label_text="Mediana Empresa"),
            create_radio(value="3", label_text="Gran Empresa"),
            create_radio(value="%", label_text="Todos (General)")
        ],)
    )


def rd_ubicacion(ubicacion):
    return RadioGroup(
        ref=ubicacion,
        value="0",
        content=Row([
            create_radio(value="0", label_text="Urbano"),
            create_radio(value="1", label_text="Rural"),
        ], alignment=MainAxisAlignment.SPACE_AROUND)
    )


def rd_estado_editar(proceso):
    return RadioGroup(
        ref=proceso,
        value="0",
        content=Row([
            create_radio(value="editar", label_text="Entregado"),
            create_radio(value="reiniciar", label_text="Reiniciar"),
        ], alignment=MainAxisAlignment.SPACE_AROUND)
    )


def rd_tipo_po(tipo_po):
    return RadioGroup(
        ref=tipo_po,
        value="0",
        content=Row([
            create_radio(value="%", label_text="Ambos"),
            create_radio(value="Apertura", label_text="Apertura"),
            create_radio(value="Renovacion", label_text="Renovacion"),
        ], alignment=MainAxisAlignment.SPACE_AROUND)
    )


def rd_tipo_impuesto(tipo_impuesto):
    return RadioGroup(
        ref=tipo_impuesto,
        value="%",
        content=Column([
            create_radio(value="0", label_text="Otras Tasas"),
            create_radio(value="1", label_text="Bienes Inmuebles"),
            create_radio(value="4", label_text="Impuesto Personal"),
            create_radio(
                value="2", label_text="Industria, Comercio y Servicio"),
            create_radio(value="3", label_text="Permiso de Operación"),
            create_radio(value="5", label_text="Servicios Públicos"),
            create_radio(value="7", label_text="Planes de Pago"),
            create_radio(value="%", label_text="Todos (General)")
        ],)
    )


def rd_tipo_entrega_apremio(tipo_res):
    return RadioGroup(
        ref=tipo_res,
        value='0',
        content=Column([
            create_radio(value="0", label_text="Entregado Personalmente"),
            create_radio(value="1", label_text="Entregado a un tercero"),
            create_radio(
                value="2", label_text="Notificado (Se dejó en la propiedad)"),
            create_radio(
                value="3", label_text="Notificado en la Municipalidad"),
            create_radio(value="4", label_text="Otro")
        ],)
    )





def rd_tipo_persona(tipo_persona):
    return RadioGroup(
        ref=tipo_persona,
        value="%",
        content=Row([
            create_radio(value="0", label_text="Persona Natural"),
            create_radio(value="1", label_text="Persona Jurídica"),
            create_radio(value="%", label_text="Todos"),
        ], alignment=MainAxisAlignment.SPACE_AROUND)
    )

def rd_tipo_rubro_ics(tipo):
    return RadioGroup(
        ref=tipo,
        value="%",
        content=Row([
            create_radio(value="0", label_text="Industria"),
            create_radio(value="1", label_text="Comercio"),
            create_radio(value="2", label_text="Servicio"),
            create_radio(value="%", label_text="Todos"),
        ], alignment=MainAxisAlignment.SPACE_AROUND)
    )



def rd_numero_firmas(value:str|None = '0', ref_num_firma:Ref|None = None)->RadioGroup:
    return RadioGroup(
        ref=ref_num_firma,
        value=value,
        content=Row([
            create_radio(value="0", label_text="1 Firma"),
            create_radio(value="1", label_text="2 Firmas"),
        ],)
    )

def rd_tamanio_documento_pdf(tipo_res:Ref |None, value=None):
    return RadioGroup(
        
        ref=tipo_res,
        value=value,
        content=Row([
            create_radio_tipo(value="MediaCarta", label_text="Media Carta"),
            create_radio_tipo(value="Carta", label_text="Carta"),
            create_radio_tipo(value="OriginalCopiaCarta", label_text="(Orginal y Copia)"),
        ],alignment=MainAxisAlignment.SPACE_EVENLY)
    )

def create_radio_tipo(value='0', label_text="") -> Container:

    con = Container(
        width=140,
        height=30,
        content=Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[Radio(value=value,
                 label=label_text,
                 label_position=LabelPosition.CENTER,
                 fill_color=color_check(),
                 label_style=TextStyle(
                     size=10, color=color_texto(), font_family="Tahoma")
                 )]
        )
    )
    return con


