import flet as ft
from src.ui.components.ui_boton_tamanio_rpt import create_boton_tamanio_pdf
from src.ui.components.ui_radio import rd_numero_firmas, rd_tamanio_documento_pdf
from src.ui.components.ui_dropbox import dropbox_departamentos

from src.utils.config_manager import Config
TIPO_REPORTE = Config.obtener("APREMIO", "tipo_documento")
NUM_FIRMAS = Config.obtener("APREMIO", "numfirmas")
DEPARTAMENTO_CARGO_1 = Config.obtener("APREMIO", "cargo_1")
DEPARTAMENTO_CARGO_2 = Config.obtener("APREMIO", "cargo_2")


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

def numero_firmas (self,vista):
    num_firmas = ft.Ref[ft.RadioGroup]()
    def handle_firmas(e):
        numfimas = num_firmas.current.value
        Config.guardar_cargo_firma(numfirmas = numfimas)
        if numfimas == '0':
            self.departamentos_2.disabled = True
        else:
            self.departamentos_2.disabled = False

        vista.update(self.departamentos_2)
            
    firmas = rd_numero_firmas(NUM_FIRMAS, num_firmas)
    firmas.on_change = handle_firmas
    
    return firmas


def list_departamentos_frm_1 (vista):
    vista.cod_depto = ft.Ref[ft.Dropdown]()
    def handle_deptos(e):
        cod_depto = vista.cod_depto.current.value
        cargo_1 = ""
        firma_1 = ""
        for fila in data_deptos:
                if fila['IdDeptos'] == dropbox_deptos.value:
                    cargo_1 = fila['DeptoDesc']
                    firma_1 = fila['IdDeptos']
                    continue
        Config.guardar_cargo_firma(cargo_1=cargo_1, firma_1=firma_1)
        

    data_deptos = [
        {'IdDeptos': "Catastro", 'DeptoDesc': 'Catastro'},
        {'IdDeptos': "Tributaria", 'DeptoDesc': 'Administración Tributaria'},
        {'IdDeptos': "Ambiental", 'DeptoDesc': 'Unidad Municipal Ambiental'},
        {'IdDeptos': "Justicia", 'DeptoDesc': 'Dirección DE Justicia Municipal'},
        {'IdDeptos': "Contabilidad", 'DeptoDesc': 'Contabilidad'},
        {'IdDeptos': "Secretaria", 'DeptoDesc': 'Secretaria'},
        {'IdDeptos': "Alcalde", 'DeptoDesc': 'Alcalde Municipal'},
        {'IdDeptos': "DesarrolloUrbano", 'DeptoDesc': 'Desarrollo Urbano'},
        {'IdDeptos': "Tesorero", 'DeptoDesc': 'Tesoreria'},
        ]

    dropbox_deptos = dropbox_departamentos(data_deptos, vista.cod_depto, DEPARTAMENTO_CARGO_1)
    dropbox_deptos.on_change = handle_deptos
    return dropbox_deptos


def list_departamentos_frm_2 (vista):
    vista.cod_depto = ft.Ref[ft.Dropdown]()
    def handle_deptos(e):
        cod_depto = vista.cod_depto.current.value
        cargo_2 = ""
        firma_2 = ""
        for fila in data_deptos:
                if fila['IdDeptos'] == dropbox_deptos.value:
                    cargo_2 = fila['DeptoDesc']
                    firma_2 = fila['IdDeptos']
                    continue
        Config.guardar_cargo_firma(cargo_2=cargo_2, firma_2=firma_2)
    data_deptos = [
        {'IdDeptos': "Catastro", 'DeptoDesc': 'Catastro'},
        {'IdDeptos': "Tributaria", 'DeptoDesc': 'Administración Tributaria'},
        {'IdDeptos': "Ambiental", 'DeptoDesc': 'Unidad Municipal Ambiental'},
        {'IdDeptos': "Justicia", 'DeptoDesc': 'Dirección DE Justicia Municipal'},
        {'IdDeptos': "Contabilidad", 'DeptoDesc': 'Contabilidad'},
        {'IdDeptos': "Secretaria", 'DeptoDesc': 'Secretaria'},
        {'IdDeptos': "Alcalde", 'DeptoDesc': 'Alcalde Municipal'},
        {'IdDeptos': "DesarrolloUrbano", 'DeptoDesc': 'Desarrollo Urbano'},
        {'IdDeptos': "Tesorero", 'DeptoDesc': 'Tesoreria'},
        ]

    dropbox_deptos = dropbox_departamentos(data_deptos, vista.cod_depto, DEPARTAMENTO_CARGO_2)
    dropbox_deptos.on_change = handle_deptos

    if NUM_FIRMAS == '0':
        dropbox_deptos.disabled = True

    return dropbox_deptos