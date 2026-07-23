# ui/reportes/vista_reportes.py

import asyncio
import flet as ft

from src.services.aldea_servives import AldeaService
from src.services.apremio_service import ApremioService
from src.services.apremio_identifiacion_services import ApremioIdentificacionService
from src.services.parametro_service import ParametroService
from src.services.contribuyente_services import ContribuyenteService
from src.ui.apremio.layout_apremio import build_layout
from src.ui.apremio.layuot_principal import build_layout_principal
from src.ui.apremio.componentes_apremio import botones_apremio, botones_contribuyente, busqueda_identificacion,botones_apremio_table,  cerate_data_general, cerate_data_general_mora, cerate_data_general_proceso, tabla_identificacion_bi, tabla_identificacion_ics, tabla_identificacion_ip, tabla_identificacion_pp, tabla_identificacion_sp, tabla_requeridos, tabla_paginacion
from src.ui.apremio.modals_apremio.editar_apremio_modal import abrir_modal_editar_apremio
from src.ui.apremio.modals_apremio.eliminar_apremio_modal import abrir_modal_eliminar_apremio
from src.ui.apremio.modals_apremio.ver_apremio_modal import abrir_modal_ver_apremio
from src.ui.modals.apremio_2_modal import abrir_modal_rpt_apremio_2do
from src.ui.modals.apremio_certificion_modal import abrir_modal_rpt_cerificacion
from src.ui.components.ui_container import container_titulo, create_container, create_container_card, create_container_tabla
from src.ui.apremio.eventos_apremio import( generar_aviso_cobro, generar_primer_requerimiento, generar_primer_requerimiento_individual, 
                                           generar_segundo_requerimiento, obtener_contriuyente, 
obtener_contriuyente_proceso, reiniciar_primer_requerimiento, generar_certificacion)
from src.ui.modals.apremio_modal import abrir_modal_rpt_apremio_1er
from src.ui.components.ui_text import txt_label_text_tabs
from src.ui.components.ui_colors import color_borde, color_texto, color_texto_2, color_bg, color_bg_2
from src.ui.apremio.layout_identifiacion import build_layout_identificacion
from src.ui.apremio.layout_contribuyente_individual import build_layout_contribuyente
from src.ui.modals.apremio_aviso_cobro import abrir_modal_aviso_cobro
borde_color = color_borde()
texto_color = color_texto()
texto_color_2 = color_texto_2()
bg_color = color_bg()
bg_color_2 = color_bg_2()


class VistaApremio:
    def __init__(self, page, context):
        self.page = page
        self.app = context
    

        self.page.theme = ft.Theme(
            scrollbar_theme=ft.ScrollbarTheme(
                thumb_color=bg_color,       # color de la barra
                track_color=texto_color,   # fondo del track
                track_border_color=bg_color_2,
                track_visibility=True,
                thickness=10,                      # grosor
                radius=10,                         # bordes redondeados
            )
        )

        # servicios y datos
        self._init_services()
        self.barra = busqueda_identificacion(self)

        # titulos
        self.titulo_apremio = container_titulo("PROCESO DE APREMIO")
        self.titulo_proceso = container_titulo("Inicar Procesos")
        self.titulo_proceso_general = container_titulo("IDENTIFICACION DE MORA")
        self.titulo_proceso_bi = container_titulo("MORA BIENES INMUEBLES")
        self.titulo_proceso_ip = container_titulo("MORA IMPUESTO PERSONAL")
        self.titulo_proceso_ics = container_titulo("MORA INDUSTRIA COMERCIO Y SERVICIOS")
        self.titulo_proceso_sp = container_titulo("MORA SERVICIOS PUBLICOS")
        self.titulo_proceso_pp = container_titulo("MORA PLANES DE PAGO")
        self.tabla = tabla_requeridos(self)
        self.tabla_identificacion_bi = tabla_identificacion_bi(self)
        self.tabla_identificacion_ics = tabla_identificacion_ics(self)
        self.tabla_identificacion_ip = tabla_identificacion_ip(self)
        self.tabla_identificacion_sp = tabla_identificacion_sp(self)
        self.tabla_identificacion_pp = tabla_identificacion_pp(self)
        self.label_identificacion = txt_label_text_tabs( "Identificacion de Mora")
        # botones
        self.contenedor_botones = create_container(botones_apremio(self))
        self.contenedor_botones_table = botones_apremio_table(self)
        self.contenedor_requeridos = create_container_tabla(self.tabla)
        self.contenedor_identificacion_bi = create_container_tabla(
            self.tabla_identificacion_bi)
        self.contenedor_identificacion_ics = create_container_tabla(
            self.tabla_identificacion_ics)
        self.contenedor_identificacion_ip = create_container_tabla(
            self.tabla_identificacion_ip)
        self.contenedor_identificacion_sp = create_container_tabla(
            self.tabla_identificacion_sp)
        self.contenedor_identificacion_pp = create_container_tabla(
            self.tabla_identificacion_pp)
        self.paginacion = tabla_paginacion(self)
        self.contenedor_paginacion = create_container(content=self.paginacion)

        # layout
        self.layout_control = build_layout(
            self.titulo_apremio,
            self.contenedor_requeridos,
            self.contenedor_botones_table,
            self.contenedor_paginacion
        )
        self.layout_proincipal = build_layout_principal(
            self.titulo_proceso,
            self.contenedor_botones
        )

        self.layout_identificacion_bi = build_layout_identificacion(self.titulo_proceso_general, self.barra,
                                                                    self.titulo_proceso_bi, self.contenedor_identificacion_bi,
                                                                    self.titulo_proceso_ip, self.contenedor_identificacion_ip,
                                                                    self.titulo_proceso_ics, self.contenedor_identificacion_ics,
                                                                    self.titulo_proceso_sp, self.contenedor_identificacion_sp)

        self.card_data = cerate_data_general(self)
        self.mora_card = cerate_data_general_mora(self)
        self.proceso_card = cerate_data_general_proceso(self)

        self.contenedor_card_data = create_container_card(self.card_data)
        self.contenedor_mora_card = create_container_card(self.mora_card)
        self.contenedor_proceso_card = create_container_card(self.proceso_card)
        self.contenedor_botones_contribuyente = create_container(
            botones_contribuyente(self))

        self.layout_contribuyente = build_layout_contribuyente(
            self, card_generales=self.contenedor_card_data,
            card_mora=self.contenedor_mora_card,
            card_proceso=self.contenedor_proceso_card, botones=self.contenedor_botones_contribuyente)

    def build(self):
        return ft.Tabs(
            selected_index=0,
            expand=1,
            unselected_label_color=texto_color,
            unselected_label_text_style=ft.TextStyle(
                size=12.5,  weight=ft.FontWeight.W_400),

            label_color=texto_color,
            label_text_style=ft.TextStyle(
                size=12.5,  weight=ft.FontWeight.W_800),

            indicator_border_radius=0.5,
            indicator_color=borde_color,
            tabs=[
                ft.Tab(
                    text="PROCESOS",
                    content=self.layout_proincipal
                ),

                ft.Tab(
                    text="CONTRIBUYENTE",
                    content=self.layout_contribuyente
                ),
                ft.Tab(
                    text="PROCESO DE APREMIO",
                    content=self.layout_control
                ),
                ft.Tab(
                    text="IDENTIFIACION DE MORA",
                    content=self.layout_identificacion_bi
                ),
            ]
        )

    def _init_services(self):
        self.datos_muni = self.app.datos_muni
        self.datos_muni_admin = self.app.datos_admin
        self.datos_system = self.app.datos_system
        self.user = self.app.usuario_actual
        self.apremio = ApremioService(
            self.app.conexion_saft, self.datos_system, self.user)
        self.apremio_identificacion = ApremioIdentificacionService(
            self.app.conexion_saft, self.datos_system, self.user)
        self.aldeas = AldeaService(self.app.conexion_saft)
        self.contribuente = ContribuyenteService(self.app.conexion_saft)
        
        self.pagina_actual = 1
        self.filas_por_pagina = 10
        self.df = []
        self.df_identificacion_mora_bi = []
        self.df_identificacion_mora_ics = []
        self.df_identificacion_mora_ip = []
        self.df_identificacion_mora_sp = []
        self.df_identificacion_mora_pp = []
        self.fecha_minima = ""
        self.val_min = 0.0
        self.cod_aldea = ""
        self.cod_barrio = ""
        self.nombre_aldea = ""
        self.nombre_barrio = ""
        self.data_contribuyente = None
        self.data_contribuyente_mora = None
        self.data_contribuyente_proceso = None
        self.identidad = ''


    def cerrar_modal(self):
        
        self.dialog.open = False
        self.page.update()

    def cambiar_pagina(self, nueva_pagina):
        self.pagina_actual = nueva_pagina
        self.actualizar_tabla()

    def cambiar_filas(self, nueva_pagina):
        self.filas_por_pagina = nueva_pagina
        self.actualizar_tabla()

    def actualizar_tabla(self, e=None):
        self.df = self.apremio.get_table_apremio()
        self.tabla = tabla_requeridos(self)
        self.paginacion = tabla_paginacion(self)
        self.contenedor_requeridos.content = create_container_tabla(self.tabla)
        self.contenedor_paginacion.content = self.paginacion
        self.page.update()

    def abril_modal_apremio_1er(self, e):
        self.tipo_impuesto = '%'
        self.tipo_persona = '%'
        self.cod_aldea = ''
        self.cod_barrio = ''
        self.nombre_aldea = ''
        self.nombre_barrio = ''
        self.num_avisos = ''
        self.mora_mayor = ''
        self.fecha_minima = ''
        self.dialog = abrir_modal_rpt_apremio_1er(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abril_modal_aviso_cobro(self, e):
            self.tipo_impuesto = '%'
            self.tipo_persona = '%'
            self.cod_aldea = ''
            self.cod_barrio = ''
            self.nombre_aldea = ''
            self.nombre_barrio = ''
            self.num_avisos = ''
            self.mora_mayor = ''
            self.fecha_minima = ''
            self.dialog = abrir_modal_aviso_cobro(self, e)
            self.page.open(self.dialog)
            self.page.update()

    def abril_modal_apremio_2do(self, e):
        self.tipo_impuesto = '%'
        self.tipo_persona = '%'
        self.cod_aldea = ''
        self.cod_barrio = ''
        self.nombre_aldea = ''
        self.nombre_barrio = ''
        self.dialog = abrir_modal_rpt_apremio_2do(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abril_modal_apremio_cerificacion(self, e):
        self.tipo_impuesto = '%'
        self.tipo_persona = '%'
        self.cod_aldea = ''
        self.cod_barrio = ''
        self.nombre_aldea = ''
        self.nombre_barrio = ''
        self.dialog = abrir_modal_rpt_cerificacion(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abrir_modal_eliminar(self, id_doc):
        self.dialog = abrir_modal_eliminar_apremio(self, id_doc)
        self.page.open(self.dialog)
        self.page.update()

    def eliminar_apremio(self, id_documento, motivo_final):
        self.apremio.eliminar_proceso(id_documento)
        self.tabla.update()

    def abrir_modal_editar(self, rila_data):
        self.fecha_entrega = ""
        self.fecha_generado = ""
        self.proceso = ""
        self.tipo_entrega = ""
        self.dialog = abrir_modal_editar_apremio(self, rila_data)
        self.page.open(self.dialog)
        self.page.update()

    def editar_apremio(self, id_documento, fecha_entrega,  motivo_final):
        self.apremio.actualizar_entrega_proceso(
            id_documento, fecha_entrega,  motivo_final)
        self.tabla.update()

    def reiniciar_apremio(self, fila, e):
        asyncio.run(reiniciar_primer_requerimiento(self, fila,self.app, e))
        self.tabla.update()

    def abrir_modal_ver(self, fila):
        self.dialog = abrir_modal_ver_apremio(self, fila)
        self.page.open(self.dialog)
        self.page.update()

    def generar_apremio_pdf_1er(self, e):
        asyncio.run(generar_primer_requerimiento(self, self.app, e))


    def generar_aviso_cobro(self, e):
            asyncio.run(generar_aviso_cobro(self, self.app, e))

    def generar_apremio_pdf_individual(self, e):
        self.tipo_doc = 1
        print(self.identidad)
        if isinstance(e, str):
            self.identidad = e
        asyncio.run(generar_primer_requerimiento_individual(self,self.app, e))

    def generar_apremio_pdf_2do(self, e):
        asyncio.run(generar_segundo_requerimiento(self,self.app, e))

    def generar_apremio_certificacion(self, e):
        asyncio.run(generar_certificacion(self, e))

    def consulta_identificacion(self, e):
        cod_aldea = self.cod_aldea.current.value
        cod_barrio = self.cod_barrio.current.value
        val_min = self.val_min.current.value
        self.df_identificacion_mora_bi = self.apremio_identificacion.obtener_identificacion_mora(
            tipo_impuesto='1',
            tipo_persona='False',
            cod_aldea=cod_aldea,
            cod_barrio=cod_barrio,
            mora_minima=val_min,
            fecha_min=self.fecha_minima
        )
        self.df_identificacion_mora_ics = self.apremio_identificacion.obtener_identificacion_mora(
            tipo_impuesto='2', tipo_persona='True',
            cod_aldea=cod_aldea,
            cod_barrio=cod_barrio,
            mora_minima=val_min,
            fecha_min=self.fecha_minima)
        self.df_identificacion_mora_ip = self.apremio_identificacion.obtener_identificacion_mora(
            tipo_impuesto='4', tipo_persona='False',
            cod_aldea=cod_aldea,
            cod_barrio=cod_barrio,
            mora_minima=val_min,
            fecha_min=self.fecha_minima)
        self.df_identificacion_mora_sp = self.apremio_identificacion.obtener_identificacion_mora(
            tipo_impuesto='5', tipo_persona='False',
            cod_aldea=cod_aldea,
            cod_barrio=cod_barrio,
            mora_minima=val_min,
            fecha_min=self.fecha_minima)
        self.df_identificacion_mora_pp = self.apremio_identificacion.obtener_identificacion_mora(
            tipo_impuesto='7', tipo_persona='False',
            cod_aldea=cod_aldea,
            cod_barrio=cod_barrio,
            mora_minima=val_min,
            fecha_min=self.fecha_minima)

        self.tabla_identificacion_bi = tabla_identificacion_bi(self)
        self.tabla_identificacion_ics = tabla_identificacion_ics(self)
        self.tabla_identificacion_ip = tabla_identificacion_ip(self)
        self.tabla_identificacion_sp = tabla_identificacion_sp(self)
        self.tabla_identificacion_pp = tabla_identificacion_pp(self)

        self.contenedor_identificacion_bi.content = create_container_tabla(
            self.tabla_identificacion_bi)
        self.contenedor_identificacion_ics.content = create_container_tabla(
            self.tabla_identificacion_ics)
        self.contenedor_identificacion_ip.content = create_container_tabla(
            self.tabla_identificacion_ip)
        self.contenedor_identificacion_sp.content = create_container_tabla(
            self.tabla_identificacion_sp)
        self.contenedor_identificacion_pp.content = create_container_tabla(
            self.tabla_identificacion_pp)
        self.page.update()

    def get_contribuyente(self, e):
        self.data_contribuyente = obtener_contriuyente(self,)
        self.data_contribuyente_proceso = obtener_contriuyente_proceso(self,)

        self.contribuyente = cerate_data_general(self,)
        self.contribuyente_mora = cerate_data_general_mora(self,)
        self.contribuyente_proceso = cerate_data_general_proceso(self)

        self.contenedor_card_data.content = create_container_card(
            self.contribuyente)
        self.contenedor_mora_card.content = create_container_card(
            self.contribuyente_mora)
        self.contenedor_proceso_card.content = create_container_card(
            self.contribuyente_proceso)
        self.page.update()
