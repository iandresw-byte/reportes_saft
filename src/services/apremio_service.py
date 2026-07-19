import webbrowser
from datetime import datetime
from decimal import Decimal
from pandas import DataFrame
import pandas as pd
from src.models.usuario_model import Usuario
from src.repositories.apremio_repository import ApremioRepository, ApremioDetalle, ApremioAvPg, ApremioEnDoc, EstadoApremio, ApremioRelacion
from src.services.parametro_service import ParametroService

from src.utils.cuentas_apremio_gob import clasificar_mora_gob
from src.utils.cuentas_apremio_sami import clasificar_mora_sami


class ApremioService:
    def __init__(self, conexion, sistem, usuario_sesion: Usuario | None):
        self.repo = ApremioRepository(conexion, sistem)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem
        self.user = usuario_sesion
        self.data_ordenada = []

    def get_tipo_impuesto(self, tipo_impuesto=None):
        if tipo_impuesto == '%':
            return "Impuestos, Tasas y Servicios Municipales"
        elif tipo_impuesto == '0':
            return "Otras Tasas y Servicios Municipales"
        elif tipo_impuesto == '1':
            return "Impuestos Sobre Bienes Inmuebles"
        elif tipo_impuesto == '2':
            return "Impuesto de Sobre Industria, Comercio y Servicio"
        elif tipo_impuesto == '3':
            return "Tasas de Permiso de Operacion"
        elif tipo_impuesto == '4':
            return "Impuesto Personal"
        elif tipo_impuesto == '5':
            return "Servicios Publicos Municipales"
        elif tipo_impuesto == '7':
            return "Planes de Pago"
        else:
            return "Otros No Clasificados"

    def obtener_mora_gob(self, tipo_impuesto='%', tipo_persona="%", cod_aldea='%', cod_barrio='%', tipo_doc=1, num_requerimiento=10, mora_minima=0.0, fecha_min=None):
        self.data_ordenada = []
        titulo_impuesto = self.get_tipo_impuesto(tipo_impuesto)
        if tipo_doc == 1:
            dato_apremio = self.repo.obtener_1er_requerimiento(tipo_impuesto=tipo_impuesto,
                                                               tipo_persona=tipo_persona,
                                                               cod_aldea=cod_aldea,
                                                               cod_barrio=cod_barrio,
                                                               num_req=num_requerimiento,
                                                               mora_minima=mora_minima,
                                                               fecha_minia=fecha_min)
        elif tipo_doc == 2:
            dato_apremio = self.repo.obtener_2do_requerimiento(tipo_impuesto=tipo_impuesto,
                                                               tipo_persona=tipo_persona,
                                                               cod_aldea=cod_aldea,
                                                               cod_barrio=cod_barrio)
            data_1er_requerimiento = self.repo.otener_ids_docuemtos(
                EstadoApremio.ENTREGADO.value, 1, tipo_impuesto)
            mapa_ids = {
                item["Identidad"]: item["IdDocumento"]
                for item in data_1er_requerimiento
            }
        elif tipo_doc == 3:
            dato_apremio = self.repo.obtener_certificacion(tipo_impuesto=tipo_impuesto,
                                                           tipo_persona=tipo_persona,
                                                           cod_aldea=cod_aldea,
                                                           cod_barrio=cod_barrio)
            data_2do_requerimiento = self.repo.otener_ids_docuemtos(
                EstadoApremio.ENTREGADO.value, 2, tipo_impuesto)
            mapa_ids_2do = {
                item["Identidad"]: item["IdDocumento"]
                for item in data_2do_requerimiento
            }
        else:
            dato_apremio = self.repo.obtener_2do_requerimiento(tipo_impuesto=tipo_impuesto,
                                                               tipo_persona=tipo_persona,
                                                               cod_aldea=cod_aldea,
                                                               cod_barrio=cod_barrio)
        for dato in dato_apremio:
            if self.sys["TpoCuenta"]:
                mora = clasificar_mora_sami(dato, tipo_impuesto)
            else:
                mora = clasificar_mora_gob(dato, tipo_impuesto)
            num_documeto = self.repo.get_num_documento()
            fila = {'dni': dato['DNI'],
                    'nombre': dato['Pnombre'] + ' ' + dato['SNombre'] + ' ' + dato['PApellido'] + ' ' + dato['SApellido'],
                    'direccion': dato['Direccion'],
                    'clave_catastro': dato['ClavesCatastro'],
                    'periodo': f"{dato['mes_ini'].strftime("%d-%m-%Y")} - {dato['mes_fin'].strftime("%d-%m-%Y")}",
                    "saldo": dato['total'],
                    "mora": mora,
                    "num_documeto": num_documeto
                    }
            if tipo_impuesto != '%':
                tipo_imp = int(tipo_impuesto)
            else:
                tipo_imp = "%"

            if tipo_doc == 1:
                self.insert_apremio_enc(
                    dato['DNI'], tipo_imp, num_documeto, cod_barrio, dato['total'])

            elif tipo_doc == 2:
                id_doc = mapa_ids.get(dato['DNI'])
                self.insert_apremio_enc(
                    dato['DNI'], tipo_imp, num_documeto, cod_barrio, dato['total'], tipo_doc)
                self.insertar_relacion_doc(num_documeto, tipo_doc, id_doc)

            elif tipo_doc == 3:
                id_doc = mapa_ids_2do.get(dato['DNI'])
                self.insert_apremio_enc(
                    dato['DNI'], tipo_imp, num_documeto, cod_barrio, dato['total'], tipo_doc)
                self.insertar_relacion_doc(num_documeto, tipo_doc, id_doc)

            else:
                self.insert_apremio_enc(
                    dato['DNI'], tipo_imp, num_documeto, cod_barrio, dato['total'])

            self.insert_factura(dato['DNI'], tipo_impuesto, num_documeto)
            self.insert_apremio_detalle(
                dato['DNI'], tipo_imp, num_documeto)
            self.data_ordenada.append(fila)
        # self.generar_pdf_apremio(titulo=titulo_impuesto)
        return self.data_ordenada

    def obtener_mora_sami(self, tipo_impuesto: None, tipo_persona: None):
        pass

 

    def insert_factura(self, identidad, tipo_impuesto, id_docuemto):
        data = self.repo.get_facturas_a_requerir(
            dni=identidad, tipo_impuesto=tipo_impuesto)
        if data:
            for factura in data:
                factura_insert = ApremioAvPg(idDocumento=id_docuemto,
                                             NumAvPg=factura["NumAvPg"],
                                             ValNumAvPg=factura["Mora"])
                self.repo.insertar_factura(factura_insert)

    def insert_apremio_enc(self, identidad: str, tipo_impuesto: int, id_docuemto: int, cod_barrio: str, total_mora: Decimal, tipo_doc=1):
        encabezado = ApremioEnDoc(
            Identidad=identidad,
            IdDocumento=id_docuemto,
            TipoDoc=tipo_doc,
            TipoImpuesto=tipo_impuesto,
            TotalMora=total_mora,
            CodBarrio=cod_barrio,
            Observacion="",)

        data = self.repo.insertar_encabezado(encabezado)

    def insert_apremio_detalle(self, identidad: str, tipo_impuesto: int, id_docuemto: int):
        if tipo_impuesto == 0:
            data_detalle = self.repo.get_os_detalle(identidad)
        elif tipo_impuesto == 1:
            data_detalle = self.repo.get_bi_detalle(identidad)
        elif tipo_impuesto == 2:
            data_detalle = self.repo.get_ics_detalle(identidad)
        elif tipo_impuesto == 4:
            data_detalle = self.repo.get_ip_detalle(identidad)
        elif tipo_impuesto == 5:
            data_detalle = self.repo.get_sp_detalle(identidad)
        elif tipo_impuesto == 7:
            data_detalle = self.repo.get_pp_detalle(identidad)
        else:
            data_detalle = []
            data = self.repo.get_os_detalle(identidad)
            if data:
                for da in data:
                    data_detalle.append(da)
            data = self.repo.get_bi_detalle(identidad)
            if data:
                for da in data:
                    data_detalle.append(da)
            data = self.repo.get_ics_detalle(identidad)
            if data:
                for da in data:
                    data_detalle.append(da)
            data = self.repo.get_ip_detalle(identidad)
            if data:
                for da in data:
                    data_detalle.append(da)
            data = self.repo.get_sp_detalle(identidad)
            if data:
                for da in data:
                    data_detalle.append(da)
            data = self.repo.get_pp_detalle(identidad)
            if data:
                for da in data:
                    data_detalle.append(da)

        if data_detalle:
            for data in data_detalle:
                encabezado = ApremioDetalle(IdDocumento=id_docuemto,
                                            TipoImpuesto=tipo_impuesto,
                                            Descripcion=data['DNI'],
                                            Observacion=data['TIPO'],
                                            Monto=data['Mora'])

                self.repo.insertar_detalle(encabezado)

    def get_table_apremio(self) -> DataFrame:
        data = self.repo.get_tabla_apremio_enc()
        estados_sql = self.repo.get_facturas_estado()
        estados_procesados = self.procesar_estados(estados_sql)
        get_2do_req_info = self.repo.otener_info_2do_requerimiento()
        get_3er_req_info = self.repo.otener_info_certificacion()
        get_1er_req_info_reversa = self.repo.otener_info_1er_requerimiento_reversa()
        get_2do_req_info_reversa = self.repo.otener_info_2do_requerimiento_reversa()
        df_estados = DataFrame(estados_procesados)
        df_2do = DataFrame(get_2do_req_info)
        df_3er = DataFrame(get_3er_req_info)

        df_2do_rev = DataFrame(get_2do_req_info_reversa)
        df_1er_rev = DataFrame(get_1er_req_info_reversa)

        if data:

            df = DataFrame(data)
            mapa_tipo_doc = {
                0: "Aviso de Cobro",
                1: "1er Requerimiento",
                2: "2do Requerimiento",
                3: "Certificación"
            }

            df["TipoDocDescripcion"] = df["TipoDoc"].map(mapa_tipo_doc)

            mapa_tipo = {
                0: "OT",
                1: "BI",
                2: "ICS",
                3: "PO",
                4: "IP",
                5: "SP",
                7: "PP",
                10: "TT"
            }
            df["TipoImpDescripcion"] = df["TipoImpuesto"].map(mapa_tipo)

            mapa_tipo_long = {
                0: "OTRAS TASAS",
                1: "BIENES INMUEBLES",
                2: "INDUSTRIA COMERCIO Y SERVICIOS",
                3: "PERMISOS DE OPERACION",
                4: "IMPUESTO PERSONAL",
                5: "SERVICIOS PUBLICOS",
                7: "PLAN DE PAGO",
                10: "TODOS LOS IMPUESTOS Y TASAS",
            }
            df["TipoImpDescripcionLong"] = df["TipoImpuesto"].map(
                mapa_tipo_long)

            df["FechaFormateadaGenerada"] = pd.to_datetime(
                df["FechaGeneracion"]).dt.strftime("%d-%m-%Y")
           # 1️⃣ Merge estados
            if not df_estados.empty:
                df = df.merge(df_estados, on="IdDocumento", how="left")
                df["Monto_act_formateado"] = df["mora_actual"].apply(
                lambda x: f"HNL. {x:,.2f}" if pd.notnull(x) else ""
                )
                df["Monto_pagado_formateado"] = df["pagado"].apply(
                lambda x: f"HNL. {x:,.2f}" if pd.notnull(x) else ""
                )
                df["Monto_anulado_formateado"] = df["anulado"].apply(
                    lambda x: f"HNL. {x:,.2f}" if pd.notnull(x) else ""
                )
                df["Monto_plan_pago_formateado"] = df["plan_pago"].apply(
                    lambda x: f"HNL. {x:,.2f}" if pd.notnull(x) else ""
                )
            else:
                valor = 0
                df["Monto_act_formateado"] = f"HNL. {valor:,.2f}"
                df["Monto_pagado_formateado"] = f"HNL. {valor:,.2f}"
                df["Monto_anulado_formateado"] =f"HNL. {valor:,.2f}"
                df["Monto_plan_pago_formateado"] = f"HNL. {valor:,.2f}"

            # 2️⃣ Merge 2do requerimiento (1ro → 2do)
            if not df_2do.empty:
                df = df.merge(df_2do, on="IdDocumento", how="left")
                df.loc[(df["TipoDoc"] == 2) & (df["Estado2do"].isna()),
                       "Estado2do"] = df["Estado"]
                df.loc[(df["TipoDoc"] == 2) & (df["TipoDoc2do"].isna()),
                       "TipoDoc2do"] = df["TipoDoc"]
                df.loc[(df["TipoDoc"] == 2) & (df["FechaEntrega2do"].isna()),
                       "FechaEntrega2do"] = df["FechaEntrega"]
                df.loc[(df["TipoDoc"] == 2) & (df["FechaGeneracion2do"].isna()),
                       "FechaGeneracion2do"] = df["FechaGeneracion"]
                df["Estado2do"] = df["Estado2do"].replace(
                    "", pd.NA).fillna("No Generado")
                df["TipoDocDescripcion2do"] = (
                    df["TipoDoc2do"].map(mapa_tipo_doc).fillna("Pendiente"))

            # 3️⃣ Merge certificación (2do → 3ro)
            df.loc[df["TipoDoc"] == 1, "Estado1er"] = df["Estado"]
            df.loc[df["TipoDoc"] == 1, "TipoDoc1er"] = df["TipoDoc"]
            df.loc[df["TipoDoc"] == 1,
                   "FechaGeneracion1er"] = df["FechaGeneracion"]
            df["TipoDocDescripcion1er"] = (
                df["TipoDoc1er"] .map(mapa_tipo_doc) .fillna("Pendiente"))

            df.loc[df["TipoDoc"] == 1, "FechaEntrega1er"] = df["FechaEntrega"]
            if not df_3er.empty:
                df = df.merge(df_3er, on="IdDocumento2do", how="left")
                df.loc[(df["TipoDoc"] == 3) & (df["Estado3er"].isna()),
                       "Estado3er"] = df["Estado"]
                df.loc[(df["TipoDoc"] == 3) & (df["TipoDoc3er"].isna()),
                       "TipoDoc3er"] = df["TipoDoc"]
                df.loc[(df["TipoDoc"] == 3) & (df["FechaEntrega3er"].isna()),
                       "FechaEntrega3er"] = df["FechaEntrega"]
                df.loc[(df["TipoDoc"] == 3) & (df["FechaGeneracion3er"].isna()),
                       "FechaGeneracion3er"] = df["FechaGeneracion"]
                df["Estado3er"] = df["Estado3er"].replace(
                    "", pd.NA).fillna("No Generado")
                df["TipoDocDescripcion3er"] = (
                    df["TipoDoc3er"] .map(mapa_tipo_doc) .fillna("Pendiente"))

            df["DiasDesdeGenerado"] = df.apply(
                lambda row: (pd.Timestamp.today() -
                             pd.to_datetime(row["FechaGeneracion"])).days
                if row["Estado"] in [EstadoApremio.GENERADO.value, EstadoApremio.PRONTO_VENCE.value]
                and pd.notnull(row["FechaGeneracion"])
                else None,
                axis=1
            )
            df["FechaFormateadaEntrega"] = df["FechaEntrega"].apply(
                lambda x: pd.to_datetime(x).strftime(
                    "%d-%m-%Y") if pd.notnull(x) else "No entregado"
            )
            ids_vencidos = df.loc[
                df["Estado"].isin([
                    EstadoApremio.GENERADO.value,
                    EstadoApremio.PRONTO_VENCE.value
                ]) &
                (df["DiasDesdeGenerado"].fillna(0) > 30),
                "IdDocumento"
            ].tolist()
            self.repo.actualizar_encabezado_estado(
                ids_vencidos, EstadoApremio.VENCIDO.value, "No se entrego despues de 30 dias de generado")
            ids_pronto = df.loc[
                (df["Estado"] == EstadoApremio.GENERADO.value) &
                (df["DiasDesdeGenerado"].between(25, 30, inclusive="both")),
                "IdDocumento"
            ].tolist()

            if ids_pronto:
                self.repo.actualizar_encabezado_estado(
                    ids_pronto,
                    EstadoApremio.PRONTO_VENCE.value,
                    "Documento próximo a vencer (25+ días)"
                )
            df.loc[df["DiasDesdeGenerado"] > 30,
                   "Estado"] = EstadoApremio.VENCIDO.value
            df.loc[df["DiasDesdeGenerado"].between(
                25, 30, inclusive="both"), "Estado"] = EstadoApremio.PRONTO_VENCE.value

            df.loc[df["Estado"] == EstadoApremio.ANULADO.value,
                   "FechaFormateadaEntrega"] = "--"
            df["DiasDesdeGenerado_fmt"] = df["DiasDesdeGenerado"].fillna("-")

            df["Monto_ini_formateado"] = df["TotalMora"].apply(
                lambda x: f"HNL. {x:,.2f}" if pd.notnull(x) else ""
            )

           

            
            df["NombreCompleto"] = (
                df["Pnombre"].fillna("") + " " +
                df["SNombre"].fillna("") + " " +
                df["PApellido"].fillna("") + " " +
                df["SApellido"].fillna("")
            ).str.replace(r"\s+", " ", regex=True).str.strip()
            # if not df_2do_rev.empty:
            #     df = df.merge(df_2do_rev, on="IdDocumento", how="left")

            # if not df_1er_rev.empty:
            #     df = df.merge(df_1er_rev, on="IdDocumento", how="left")

            df["DNI_Formateado"] = df["Identidad"].apply(
                lambda x: (
                    f"{str(x)[:4]}-{str(x)[4:8]}-{str(x)[8:]}"
                    if pd.notnull(x) and str(x).isdigit() and len(str(x)) == 13
                    else (str(x) if pd.notnull(x) else "")
                )
            )

            return df

    def tipo_doc_str(self, tipo_doc):
        if tipo_doc == 0:
            return "Aviso de Cobro"
        elif tipo_doc == 1:
            return "1er Requerimiento"
        elif tipo_doc == 2:
            return "2do Requerimiento"
        elif tipo_doc == 3:
            return "Certificacion"
        else:
            return "No Definido"

    def eliminar_proceso(self, id_documento):
        self.repo.eliminar_factura(id_documento)
        self.repo.eliminar_detalle(id_documento)
        self.repo.actualizar_encabezado_estado(
            [id_documento], EstadoApremio.ANULADO.value, f"Proceso Anulado pro el Usuario {self.user.username}")

    def insertar_relacion_doc(self, id_documento, tipo_doc, id_requerimiento):
        relacion = ApremioRelacion(
            id_documento, tipo_doc, id_requerimiento
        )
        self.repo.insertar_apremio_relacion(relacion)

    def reinicar_proceso(self, data):
        self.repo.eliminar_factura(data["IdDocumento"])
        self.repo.eliminar_detalle(data["IdDocumento"])
        cod_aldea = data["CodAldea"]
        cod_barrio = data['CodBarrio']
        if data['Tipo']:
            tipo_persona = '1'
        else:
            tipo_persona = '0'
        fecha_now = datetime.now()
        self.repo.actaulizar_reiniciar_proceso(
            data["IdDocumento"], fecha_now,  'Reinicio de Proceso', data['TotalMora'])
        self.insert_apremio_detalle(
            data['Identidad'], data['TipoImpuesto'], data["IdDocumento"],)
        self.insert_factura(data['Identidad'],
                            data['TipoImpuesto'], data["IdDocumento"],)

        if data["TipoDoc"] == 1:
            dato_apremio = self.repo.obtener_1er_requerimiento(tipo_impuesto=data['TipoImpuesto'],
                                                               tipo_persona=tipo_persona,
                                                               cod_aldea=cod_aldea,
                                                               dni=data["Identidad"],
                                                               cod_barrio=cod_barrio)
        elif data["TipoDoc"] == 2:
            dato_apremio = self.repo.obtener_2do_requerimiento(tipo_impuesto=data['TipoImpuesto'],
                                                               tipo_persona=tipo_persona,
                                                               cod_aldea=cod_aldea,
                                                               dni=data["Identidad"],
                                                               cod_barrio=cod_barrio)
        else:
            dato_apremio = self.repo.obtener_2do_requerimiento(tipo_impuesto=data['TipoImpuesto'],
                                                               tipo_persona=tipo_persona,
                                                               cod_aldea=cod_aldea,
                                                               dni=data["Identidad"],
                                                               cod_barrio=cod_barrio)
        data_ordenada = []
        self.repo.actaulizar_reiniciar_TipoImpuesto(
            data["IdDocumento"], data['TipoImpuesto'])
        for dato in dato_apremio:
            if self.sys["TpoCuenta"]:
                mora = clasificar_mora_sami(dato,  data['TipoImpuesto'])
            else:
                mora = clasificar_mora_gob(dato,  data['TipoImpuesto'])
            num_documeto = self.repo.get_num_documento()
            fila = {'dni': dato['DNI'],
                    'nombre': dato['Pnombre'] + ' ' + dato['SNombre'] + ' ' + dato['PApellido'] + ' ' + dato['SApellido'],
                    'direccion': dato['Direccion'],
                    'clave_catastro': dato['ClavesCatastro'],
                    'periodo': f"{dato['mes_ini'].strftime("%d-%m-%Y")} - {dato['mes_fin'].strftime("%d-%m-%Y")}",
                    "saldo": dato['total'],
                    "mora": mora,
                    "num_documeto": num_documeto
                    }
            if data['TipoImpuesto'] != '%':
                tipo_imp = int(data['TipoImpuesto'])
            else:
                tipo_imp = "%"
            self.insert_apremio_enc(
                dato['DNI'], tipo_imp, num_documeto, data['CodBarrio'], dato['total'])
            self.insert_factura(
                dato['DNI'], data['TipoImpuesto'], num_documeto)
            self.insert_apremio_detalle(dato['DNI'], tipo_imp, num_documeto)
            data_ordenada.append(fila)
        return data_ordenada

    def actualizar_entrega_proceso(self, id_documento, fecha, observacion):
        self.repo.actaulizar_encabezado_entrega(
            IdDocumento=id_documento, fecha_entrega=fecha, estado="Entregado", observacion=observacion)

    def procesar_estados(self, estados_sql):
        resultados = []

        for row in estados_sql:

            mora_act = row["mora_actual"] or 0
            mora_ant = row["mora_anterior"] or 0
            pagado = row["pagado"] or 0
            anulado = row["anulado"] or 0
            plan_pago = row["plan_pago"] or 0

            # PRIORIDAD
            if anulado > 0:
                estado = "Las facturas han sido anuladas" if mora_act == 0 else "Anuladas parcialmente"

            elif plan_pago > 0:
                estado = "Incluidas en plan de pago" if mora_act == 0 else "Plan de pago parcial"

            elif pagado > 0:
                estado = "Facturas pagadas" if mora_act == 0 else "Pagadas parcialmente"

            elif mora_act == mora_ant:
                estado = "Se conserva la mora"

            elif mora_act > mora_ant:
                estado = "La mora ha incrementado"

            else:
                estado = "La mora ha disminuido"

            row["estado"] = estado
            resultados.append(row)

        return resultados

    def iniar_proceso_individual(self, data, tipo_doc, identidad=None):
        if data:
            dni = data["DNI"]
        elif identidad:
            dni = identidad
        else:
            raise ValueError("No hay identidad")
        cod_aldea = '%'
        cod_barrio = '%'
        tipo_persona = '%'
        tipo_impuesto = '%'
        if tipo_doc == 1:
            dato_apremio = self.repo.obtener_1er_requerimiento(tipo_impuesto=tipo_impuesto,
                                                               tipo_persona=tipo_persona,
                                                               cod_aldea=cod_aldea,
                                                               dni=dni,
                                                               cod_barrio=cod_barrio)
        elif tipo_doc == 2:
            dato_apremio = self.repo.obtener_2do_requerimiento(tipo_impuesto=tipo_impuesto,
                                                               tipo_persona=tipo_persona,
                                                               cod_aldea=cod_aldea,
                                                               dni=dni,
                                                               cod_barrio=cod_barrio)
        else:
            dato_apremio = self.repo.obtener_2do_requerimiento(tipo_impuesto=tipo_impuesto,
                                                               tipo_persona=tipo_persona,
                                                               cod_aldea=cod_aldea,
                                                               dni=dni,
                                                               cod_barrio=cod_barrio)
        self.data_ordenada = []
        if tipo_impuesto == '%':
            tipo_impuesto = 10

        for dato in dato_apremio:
            if self.sys["TpoCuenta"]:
                mora = clasificar_mora_sami(dato, tipo_impuesto)
            else:
                mora = clasificar_mora_gob(dato, tipo_impuesto)
            num_documeto = self.repo.get_num_documento()
            fila = {'dni': dato['DNI'],
                    'nombre': dato['Pnombre'] + ' ' + dato['SNombre'] + ' ' + dato['PApellido'] + ' ' + dato['SApellido'],
                    'direccion': dato['Direccion'],
                    'clave_catastro': dato['ClavesCatastro'],
                    'periodo': f"{dato['mes_ini'].strftime("%d-%m-%Y")} - {dato['mes_fin'].strftime("%d-%m-%Y")}",
                    "saldo": dato['total'],
                    "mora": mora,
                    "num_documeto": num_documeto
                    }

            self.insert_apremio_enc(
                dato['DNI'], tipo_impuesto, num_documeto, cod_barrio, dato['total'])

            self.insert_factura(
                dato['DNI'], tipo_impuesto, num_documeto)
            self.insert_apremio_detalle(
                dato['DNI'], tipo_impuesto, num_documeto)
            self.data_ordenada.append(fila)
        # self.generar_pdf_apremio(titulo=titulo_impuesto)
        return self.data_ordenada
