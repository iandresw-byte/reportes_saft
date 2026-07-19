import flet as ft
from src.ui.components.ui_boton_tamanio_rpt import create_boton_tamanio_pdf
from src.ui.components.ui_radio import rd_numero_firmas, rd_tamanio_documento_pdf
from src.utils.config_manager import Config
TIPO_REPORTE = Config.obtener("APREMIO", "tipo_documento")

def botones_tamanio_pdf(vista, app):
    ref = ft.Ref[ft.RadioGroup]()
   

    def on_clic_boton(e:ft.ControlEvent):
        if e.control.key ==1:
            tipo = "MediaCarta"
        elif e.control.key ==2:
                tipo = "Carta"
        elif e.control.key ==3:
             tipo = "OriginalCopiaCarta"
        else:
            tipo = "Carta"
        
        rd_tipo.value = tipo
        Config.guardar_tamanio_reporte(tipo)
        app.tamanio_documento = tipo
        vista.update(rd_tipo)
        
        

    rd_tipo = rd_tamanio_documento_pdf(tipo_res=ref, value=TIPO_REPORTE)

    return ft.Column([
        ft.Row([
            create_boton_tamanio_pdf("MediaCarta", Key=1, icono=ft.Icons.DESCRIPTION_OUTLINED,tooltip="Documento orginal un una hoja yamaño media carta", data="MediaCarta", on_click=on_clic_boton),
            create_boton_tamanio_pdf("Carta",Key=2, icono=ft.Icons.ARTICLE_OUTLINED,tooltip="Documento orginal en una hoja tamaño carta", data="Carta", on_click=on_clic_boton),
            create_boton_tamanio_pdf("OriginalCopiaCarta", Key=3,icono=ft.Icons.FEED_OUTLINED,tooltip="Documento orginal y una copia en una hoja tamaño carta", data="OriginalCopiaCarta", on_click=on_clic_boton)],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            rd_tipo
            ],
        alignment=ft.MainAxisAlignment.CENTER
    )

def numero_firmas (vista):
    ref = ft.Ref[ft.RadioGroup]()
    return ft.Row([rd_numero_firmas(ref)])