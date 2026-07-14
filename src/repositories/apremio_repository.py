from datetime import datetime
from decimal import Decimal
from src.models.apremio_models import ApremioAvPg, ApremioDetalle, ApremioEnDoc, EstadoApremio, ApremioRelacion
from src.database.consultas.apremio_requerimiento_1 import *
from src.database.consultas.apremio_requerimiento_2 import *
from src.database.consultas.apremio_certificacion import *

class ApremioRepository:
    def __init__(self, conexion, sistem):
        self.conexion = conexion
        self.sys = sistem

    def obtener_1er_requerimiento(self, tipo_impuesto: str, tipo_persona: str, cod_aldea: str, cod_barrio: str, dni='%', num_req=10, mora_minima=0.0,
                                  fecha_minia=None):
        if tipo_impuesto == 10:
            tipo_impuesto = "%"  # type: ignore

        if not fecha_minia:
            fecha_minia = datetime.now().strftime("%Y%m%d")
    
        if not self.sys["TpoCuenta"]:
            query_nat = CONSULTA_APREMIO_GOB_NAT
            query_ics_nat = CONSULTA_APREMIO_GOB_ICS_X_NAT
            query_ics = CONSULTA_APREMIO_GOB_ICS_JUR
        else:
            query_nat = CONSULTA_APREMIO_SAMI_NAT
            query_ics_nat = CONSULTA_APREMIO_SAMI_ICS_X_NAT
            query_ics = CONSULTA_APREMIO_SAMI_ICS_JUR

        if tipo_impuesto == '2' and tipo_persona == '0':
            query = query_ics
            variables = (num_req, fecha_minia, tipo_impuesto, fecha_minia, cod_aldea,
                         cod_barrio, dni, mora_minima)
        elif tipo_impuesto == '2' and tipo_persona == '1':
            query = query_ics_nat
            variables = (num_req, fecha_minia, tipo_impuesto, fecha_minia,  cod_aldea,
                         cod_barrio, dni, mora_minima)
        else:
            query = query_nat
            variables = (num_req, fecha_minia, tipo_impuesto,  fecha_minia, tipo_impuesto, tipo_persona,
                         cod_aldea, cod_barrio, dni, mora_minima)

        with self.conexion.cursor() as cur:

            cur.execute(query, variables)
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def obtener_2do_requerimiento(self, tipo_impuesto: str, tipo_persona: str, cod_aldea: str, cod_barrio: str, dni='%', num_req=10):
        if tipo_impuesto == '%':
            tipo_impuesto = '10'
        
        if not self.sys["TpoCuenta"]:
            query_nat = CONSULTA_REQ2_NATURAL_GOB
            query_ics = CONSULTA_REQ2_JURIDICO_GOB
            query_ics_nat = CONSULTA_REQ2_ICS_X_NATURAL_GOB
        else:
            query_nat = CONSULTA_REQ2_NATURAL_SAMI
            query_ics = CONSULTA_REQ2_JURIDICO_SAMI
            query_ics_nat = CONSULTA_REQ2_ICS_X_NATURAL_SAMI

        if tipo_impuesto == '2' and tipo_persona == '0':
            query = query_ics
            variables = (cod_aldea, cod_barrio, dni)
        elif tipo_impuesto == '2' and tipo_persona == '1':
            query = query_ics_nat
            variables = (cod_aldea, cod_barrio, dni)
        else:
            query = query_nat
            variables = (tipo_impuesto, tipo_persona,
                         cod_aldea, cod_barrio)

        print(variables)

        with self.conexion.cursor() as cur:
            cur.execute(query, variables)
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def obtener_certificacion(self, tipo_impuesto: str, tipo_persona: str, cod_aldea: str, cod_barrio: str, dni='%', num_req=10):

        if not self.sys["TpoCuenta"]:
            query_nat = CONSULTA_CERTIFICACION_NATURAL_GOB
            query_ics = CONSULTA_CERTIFICACION_JURIDICO_GOB
            query_ics_nat = CONSULTA_CERTIFICACION_ICS_X_NATURAL_GOB
        else:
            query_nat = CONSULTA_CERTIFICACION_NATURAL_SAMI
            query_ics = CONSULTA_CERTIFICACION_JURIDICO_SAMI
            query_ics_nat = CONSULTA_CERTIFICACION_ICS_X_NATURAL_SAMI

        

        if tipo_impuesto == '2' and tipo_persona == '0':
            query = query_ics
            variables = (num_req, cod_aldea, cod_barrio, dni)
        elif tipo_impuesto == '2' and tipo_persona == '1':
            query = query_ics_nat
            variables = (num_req, cod_aldea, cod_barrio, dni)
        else:
            query = query_nat
            variables = (num_req,  tipo_impuesto, tipo_persona,
                         cod_aldea, cod_barrio, dni)
        with self.conexion.cursor() as cur:
            cur.execute(query, variables)
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def otener_ids_docuemtos(self, estado, tipo_doc, tipo_impuesto):

        query = """SELECT      Identidad, IdDocumento
                    FROM            ApremioEnDoc
                    WHERE        (Estado = ?) AND (TipoDoc like ?) AND (TipoImpuesto like ?)"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (estado, tipo_doc, tipo_impuesto))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def otener_info_2do_requerimiento(self,):
        query = """SELECT  ApremioRelacion.IdDocumento as IdDocumento2do, 
    ApremioRelacion.Id1erRequerimiento as IdDocumento, 
    ApremioRelacion.TipoDoc AS TipoDoc2do, 
    ApremioEnDoc.Estado AS Estado2do,
    ApremioEnDoc.FechaGeneracion AS FechaGeneracion2do,
    ApremioEnDoc.FechaEntrega AS FechaEntrega2do
                    FROM ApremioRelacion INNER JOIN
                    ApremioEnDoc ON ApremioRelacion.IdDocumento = ApremioEnDoc.IdDocumento
                    WHERE        (ApremioRelacion.TipoDoc = 2)
                """
        with self.conexion.cursor() as cur:
            cur.execute(query,)
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def otener_info_2do_requerimiento_reversa(self,):
        query = """SELECT  ApremioRelacion.IdDocumento, ApremioRelacion.Id1erRequerimiento AS IdDocumento2do, ApremioEnDoc.TipoDoc AS TipoDoc2do, ApremioEnDoc.Estado AS Estado2do, 
                ApremioEnDoc.FechaGeneracion AS FechaGeneracion2do, ApremioEnDoc.FechaEntrega AS FechaEntrega2do
                FROM  ApremioRelacion INNER JOIN
                ApremioEnDoc ON ApremioRelacion.Id1erRequerimiento = ApremioEnDoc.IdDocumento
                WHERE  (ApremioRelacion.TipoDoc = 3)
                """
        with self.conexion.cursor() as cur:
            cur.execute(query,)
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def otener_info_1er_requerimiento_reversa(self,):
        query = """SELECT  ApremioRelacion.IdDocumento, ApremioRelacion.Id1erRequerimiento AS IdDocumento1er, ApremioEnDoc.TipoDoc AS TipoDoc1er, ApremioEnDoc.Estado AS Estado1er, 
                ApremioEnDoc.FechaGeneracion AS FechaGeneracion1er, ApremioEnDoc.FechaEntrega AS FechaEntrega1er
                FROM  ApremioRelacion INNER JOIN
                ApremioEnDoc ON ApremioRelacion.Id1erRequerimiento = ApremioEnDoc.IdDocumento
                WHERE  (ApremioRelacion.TipoDoc = 2)
                """
        with self.conexion.cursor() as cur:
            cur.execute(query,)
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def otener_info_certificacion(self,):
        query = """SELECT  ApremioRelacion.IdDocumento as IdDocumento3er, 
    ApremioRelacion.Id1erRequerimiento as IdDocumento2do, 
    ApremioRelacion.TipoDoc AS TipoDoc3er, 
    ApremioEnDoc.Estado AS Estado3er,
    ApremioEnDoc.FechaGeneracion AS FechaGeneracion3er,
    ApremioEnDoc.FechaEntrega AS FechaEntrega3er
                    FROM ApremioRelacion INNER JOIN
                    ApremioEnDoc ON ApremioRelacion.IdDocumento = ApremioEnDoc.IdDocumento
                    WHERE        (ApremioRelacion.TipoDoc = 3)
                """
        with self.conexion.cursor() as cur:
            cur.execute(query,)
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def insertar_encabezado(self, encabezado: ApremioEnDoc):
        query = """INSERT INTO ApremioEnDoc  ( Identidad, IdDocumento, TipoDoc, TipoImpuesto, FechaGeneracion, FechaEntrega, Estado, TotalMora, CodBarrio, Observacion) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        if encabezado.TipoImpuesto == '%':
            tipo_impuesto = 10
        else:
            tipo_impuesto = encabezado.TipoImpuesto
        with self.conexion.cursor() as cur:
            cur.execute(query, (encabezado.Identidad, encabezado.IdDocumento, encabezado.TipoDoc, tipo_impuesto, encabezado.FechaGeneracion,
                        encabezado.FechaEntrega, encabezado.Estado, encabezado.TotalMora, encabezado.CodBarrio, encabezado.Observacion))
            return True

    def insertar_factura(self, factura: ApremioAvPg):
        query = """INSERT INTO ApremioAvPg (idDocumento, NumAvPg, ValNumAvPg) VALUES (?,?,?)"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (factura.idDocumento,
                        factura.NumAvPg, factura.ValNumAvPg))
            return True

    def insertar_apremio_relacion(self, relacion: ApremioRelacion):
        query = """INSERT INTO ApremioRelacion ( IdDocumento, TipoDoc, Id1erRequerimiento) VALUES (?,?,?)"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (relacion.IdDocumento,
                        relacion.TipoDoc, relacion.Id1erRequerimiento))
            return True

    def insertar_detalle(self, detalle: ApremioDetalle):
        if detalle.TipoImpuesto == '%':
            tipo_impuesto = 10
        else:
            tipo_impuesto = detalle.TipoImpuesto
        query = """INSERT INTO ApremioDetalle (IdDocumento, TipoImpuesto, Descripcion, Observacion, Monto) VALUES (?, ?, ?, ?, ?);"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (detalle.IdDocumento, tipo_impuesto,
                        detalle.Descripcion, detalle.Observacion, detalle.Monto,))
            return True

    def actaulizar_encabezado_entrega(self, IdDocumento: int, fecha_entrega: datetime, estado: str, observacion: str):
        query = """UPDATE ApremioEnDoc SET FechaEntrega = ? , Estado = ? , Observacion = ISNULL(Observacion, '') +
                      CASE WHEN Observacion IS NULL OR Observacion = ''
                           THEN ?
                           ELSE ' | ' + ?
                      END WHERE (IdDocumento = ?);"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_entrega, estado,
                        observacion, observacion, IdDocumento))
            return True

    def actualizar_encabezado_estado(self, id_documentos: list, estado: str, obs: str):

        if not id_documentos:
            return False

        placeholders = ",".join("?" for _ in id_documentos)

        query = f"""
            UPDATE ApremioEnDoc
            SET Estado = ?,
                Observacion = ISNULL(Observacion, '') +
                    CASE 
                        WHEN Observacion IS NULL OR Observacion = ''
                        THEN ?
                        ELSE ' | ' + ?
                    END
            WHERE IdDocumento IN ({placeholders})
        """

        params = [estado, obs, obs] + id_documentos

        with self.conexion.cursor() as cur:
            cur.execute(query, params)
        return True

    def actaulizar_reiniciar_proceso(self, IdDocumento: int, fecha_generacion: datetime, observacion: str, mora: Decimal):
        query = """UPDATE ApremioEnDoc SET  FechaGeneracion = ?, TipoImpuesto = 100, Estado = 'Generado', TotalMora = ?, Observacion = ISNULL(Observacion, '') +
                      CASE WHEN Observacion IS NULL OR Observacion = ''
                           THEN ?
                           ELSE ' | ' + ?
                      END WHERE (IdDocumento = ?);"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_generacion, mora,
                        observacion, observacion, IdDocumento))
            return True

    def actaulizar_reiniciar_TipoImpuesto(self, IdDocumento: int, tipo_impuesto: int):
        query = """UPDATE ApremioEnDoc SET   TipoImpuesto = ? WHERE (IdDocumento = ?);"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (tipo_impuesto, IdDocumento))
            return True

    def eliminar_encabezado(self, IdDocumento: int):
        query = """DELETE ApremioEnDoc  WHERE (IdDocumento = ?);"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (IdDocumento))
            return True

    def eliminar_factura(self,  IdDocumento: int):
        query = """DELETE ApremioAvPg  WHERE (IdDocumento = ?);"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (IdDocumento))
            return True

    def eliminar_detalle(self,  IdDocumento: int):
        query = """DELETE ApremioDetalle WHERE (IdDocumento = ?);"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (IdDocumento))
            return True

    def get_facturas_a_requerir(self, dni: str, tipo_impuesto: int):
        query = """SELECT        F_01.NumAvPg, 
                CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT) AS Mora
                FROM F_01 INNER JOIN
                F_02 ON F_01.NumAvPg = F_02.NumAvPg
                WHERE (F_01.DNI LIKE ?) AND (F_01.AvPgEstado = 1) AND (F_01.FechaVenceAvPg < GETDATE()) AND (F_01.AvPgTipoImpuesto LIKE ?)
                GROUP BY F_01.NumAvPg;
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (dni, tipo_impuesto,))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def get_os_detalle(self, dni: str):
        query = """SELECT  CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT)  AS Mora, F_01.DNI, 'OS' AS TIPO
                FROM  F_01 INNER JOIN
                F_02 ON F_01.NumAvPg = F_02.NumAvPg
                WHERE (F_01.DNI LIKE ?) AND (F_01.AvPgEstado = 1) AND (F_01.FechaVenceAvPg < GETDATE()) AND (F_01.AvPgTipoImpuesto LIKE 0)
                GROUP BY F_01.DNI;
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (dni,))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def get_bi_detalle(self, dni: str,):
        query = """SELECT CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT)  AS Mora, F_02.ClaveCatastro as DNI, 'BI' AS TIPO
                    FROM F_01 INNER JOIN
                    F_02 ON F_01.NumAvPg = F_02.NumAvPg
                WHERE (F_01.DNI LIKE ?) AND (F_01.AvPgEstado = 1) AND (F_01.FechaVenceAvPg < GETDATE()) AND (F_01.AvPgTipoImpuesto LIKE 1) and F_02.ClaveCatastro is not null
                    GROUP BY F_02.ClaveCatastro;
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (dni,))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def get_ics_detalle(self, dni: str,):
        query = """SELECT        CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT)  AS Mora, F_01.DNI, 'ICS' AS TIPO

                    FROM            F_01 INNER JOIN
                    F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
                    FC_03 ON F_01.DNI = FC_03.DNI
                    WHERE        (F_01.AvPgEstado = 1) AND (F_01.FechaVenceAvPg < GETDATE()) AND (F_01.AvPgTipoImpuesto IN (2,3)) AND (FC_03.IdRepresentante = ?)
                    GROUP BY F_01.DNI;
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (dni,))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def get_ip_detalle(self, dni: str,):
        query = """SELECT        CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT)  AS Mora, F_01.DNI, 'IP' AS TIPO

                FROM  F_01 INNER JOIN
                F_02 ON F_01.NumAvPg = F_02.NumAvPg
                WHERE (F_01.DNI LIKE ?) AND (F_01.AvPgEstado = 1) AND (F_01.FechaVenceAvPg < GETDATE()) AND (F_01.AvPgTipoImpuesto LIKE 4)
                GROUP BY F_01.DNI;
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (dni,))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def get_sp_detalle(self, dni: str,):
        query = """SELECT CAST(sum(F_02.ValorUnitAvPgDet) AS FLOAT)  AS Mora, F_01.CodDeclara AS DNI, 'SP' AS TIPO
                    FROM F_01 INNER JOIN
                    F_02 ON F_01.NumAvPg = F_02.NumAvPg
                    WHERE  (F_01.DNI LIKE ?) and (F_01.AvPgEstado = 1) AND (F_01.FechaVenceAvPg < GETDATE()) AND (F_01.AvPgTipoImpuesto LIKE 5)
                    GROUP BY  F_01.CodDeclara;
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (dni,))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def get_pp_detalle(self, dni: str,):
        query = """SELECT   CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT)  AS Mora,  F_02.ClaveCatastro as DNI , 'PP' AS TIPO
                FROM  F_01 INNER JOIN
                F_02 ON F_01.NumAvPg = F_02.NumAvPg
                WHERE (F_01.DNI LIKE ?) AND (F_01.AvPgEstado = 1) AND (F_01.FechaVenceAvPg < GETDATE()) AND (F_01.AvPgTipoImpuesto LIKE 7)
                GROUP BY F_01.DNI, F_02.ClaveCatastro;
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (dni,))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def get_num_documento(self,):
        query = """SELECT  MAX(IdDocumento) AS num_docu FROM  ApremioEnDoc"""
        with self.conexion.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            if not row[0]:
                return 1
            return int(row[0])+1

    def get_tabla_apremio_enc(self):
        query = """SELECT  ApremioEnDoc.Identidad, ApremioEnDoc.TipoDoc, ApremioEnDoc.IdDocumento, ApremioEnDoc.TipoImpuesto, ApremioEnDoc.FechaGeneracion, ApremioEnDoc.FechaEntrega, ApremioEnDoc.Estado, CAST(ApremioEnDoc.TotalMora AS FLOAT) AS TotalMora, 
                         ApremioEnDoc.CodBarrio AS Expr10, ApremioEnDoc.Observacion, FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.Direccion, FC_03.Telefono, FC_03.CodPostal, FC_03.Sexo, 
                         FC_03.FechaNac, FC_03.Tipo, FC_03.IdRepresentante, FC_03.Actividad, FC_03.NoEmpleados, FC_03.Exento, FC_03.RazonExento, FC_03.ClaveCatastro, FC_03.CodBarrio, FC_03.FechaUltRenovacion, FC_03.CodProfesion, 
                         FC_03.CodAldea, FC_03.Constitucion, FC_03.UltPeriodoFact, FC_03.UltMesFact, FC_03.Activo, FC_03.Email, FC_03.TpoDoc, FC_03.RTN, FC_03.NoContrato, FC_03.Obs, FC_03.NoCuenta, FC_03.Observaciones, FC_03.Telefono2, 
                         FC_03.NombreSociedad, FC_03.Empresa, FC_03.Insti, FC_03.Expediente, FC_03.Extendida, FC_03.FechaVence, FC_03.Nacionalidad, FC_03.FechaConstitucion, FC_03.Inscripcion
                            FROM ApremioEnDoc INNER JOIN
                        FC_03 ON ApremioEnDoc.Identidad = FC_03.DNI
                        WHERE ApremioEnDoc.Estado <> 'Anulado';
                """
        with self.conexion.cursor() as cur:
            cur.execute(query,)
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def get_facturas_estado(self,):
        query = """SELECT 
                        A.IdDocumento,
                        CAST(SUM(CASE WHEN F.AvPgEstado = '1' THEN D.SaldoActual ELSE 0 END) AS FLOAT) AS mora_actual,
                        CAST(SUM(CASE WHEN F.AvPgEstado = '1' THEN A.ValNumAvPg ELSE 0 END) AS FLOAT) AS mora_anterior,
                        CAST(SUM(CASE WHEN F.AvPgEstado = '2' THEN D.SaldoActual ELSE 0 END) AS FLOAT) AS pagado,
                        CAST(SUM(CASE WHEN F.AvPgEstado = '3' THEN D.SaldoActual ELSE 0 END) AS FLOAT) AS anulado,
                        CAST(SUM(CASE WHEN F.AvPgEstado = '6' THEN D.SaldoActual ELSE 0 END) AS FLOAT) AS plan_pago
                    FROM ApremioAvPg A
                    INNER JOIN F_01 F 
                        ON A.NumAvPg = F.NumAvPg
                    INNER JOIN (
                            SELECT NumAvPg, CAST(SUM(ValorUnitAvPgDet) AS FLOAT)  AS SaldoActual
                            FROM F_02
                            GROUP BY NumAvPg
                    ) D 
                        ON F.NumAvPg = D.NumAvPg
                    GROUP BY A.idDocumento
                """
        with self.conexion.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

            if not rows:
                return []

            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def get_proceso(self,):
        query = """SELECT IdDocumento, Identidad, TipoDoc, TipoImpuesto, FechaGeneracion, FechaEntrega, Estado, TotalMora, CodBarrio, Observacion
                    FROM  ApremioEnDoc
                    WHERE (Identidad = ?) and estado <> 'Vencido'
                """
        with self.conexion.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

            if not rows:
                return []

            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]
