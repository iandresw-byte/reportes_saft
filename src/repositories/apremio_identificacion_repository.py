
from datetime import date


class ApremioIdentifiacionRepository:
    def __init__(self, conexion) -> None:
        self.conexion = conexion

    def obtener_top10_mora(self, fecha_minimo, tipo_impuesto='1', persona='False', cod_aldea='070301', cod_barrio='070301001', valor_min=0.0):
        if fecha_minimo:
            if not isinstance(fecha_minimo, str):
                fecha_minimo = fecha_minimo.strftime('%Y%m%d')
        else:
            fecha_minimo = date.today().strftime('%Y%m%d')
        tipo_impuesto = int(tipo_impuesto)
        query = """
                SELECT TOP (10) FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.Direccion, MIN(F_01.FechaVenceAvPg) AS mes_ini, MAX(F_01.FechaVenceAvPg) AS mes_fin, 
                CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT) AS total
                FROM F_01 INNER JOIN
                FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
                F_02 ON F_01.NumAvPg = F_02.NumAvPg
                WHERE (F_01.AvPgEstado = 1) AND (F_01.FechaVenceAvPg < ?) AND (F_01.AvPgTipoImpuesto = ?)  AND (FC_03.CodAldea like ?) AND (FC_03.CodBarrio like ?) AND (NOT EXISTS
                (SELECT   1 AS Expr1
                FROM ApremioEnDoc AS A
                WHERE (Identidad = FC_03.DNI) AND (TipoImpuesto = F_01.AvPgTipoImpuesto) AND (Estado <> 'Anulado')))
                GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.Direccion
                HAVING (CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT) > ?)
                ORDER BY FC_03.DNI
            """
        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_minimo, tipo_impuesto,
                                cod_aldea, cod_barrio, valor_min))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def obtener_top10_mora_ics(self, fecha_minimo,  cod_aldea='%', cod_barrio='%', valor_min=0.0):
        if fecha_minimo:
            if not isinstance(fecha_minimo, str):
                fecha_minimo = fecha_minimo.strftime('%Y%m%d')
        else:
            fecha_minimo = date.today().strftime('%Y%m%d')
        query = """
                SELECT TOP (10) FC_03.DNI AS RTM, MIN(F_01.FechaVenceAvPg) AS mes_ini, MAX(F_01.FechaVenceAvPg) AS mes_fin, CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT) AS total, FC_03.Pnombre AS Establecimiento, FC_03_1.DNI, 
                FC_03_1.Pnombre, FC_03_1.SNombre, FC_03_1.PApellido, FC_03_1.SApellido
                FROM  F_01 INNER JOIN
                FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
                F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
                FC_03 AS FC_03_1 ON FC_03.IdRepresentante = FC_03_1.DNI
                WHERE (F_01.AvPgEstado = 1) AND (F_01.FechaVenceAvPg < ?) AND (F_01.AvPgTipoImpuesto IN (2, 3)) AND (FC_03.CodAldea = ?) AND (FC_03.CodBarrio = ?) AND (NOT EXISTS
                (SELECT 1 AS Expr1 FROM ApremioEnDoc AS A WHERE (Identidad = FC_03.DNI) AND (TipoImpuesto = F_01.AvPgTipoImpuesto) AND (Estado <> 'Anulado')))
                GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03_1.DNI, FC_03_1.Pnombre, FC_03_1.SNombre, FC_03_1.PApellido, FC_03_1.SApellido
                HAVING (CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT) > ?)
                ORDER BY RTM
            """
        with self.conexion.cursor() as cur:
            cur.execute(
                query, (fecha_minimo,   cod_aldea, cod_barrio, valor_min))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def otener_info_1er_req_by_dni(self, dni):
        query = """SELECT ApremioRelacion.IdDocumento, ApremioRelacion.Id1erRequerimiento , ApremioEnDoc.TipoDoc , ApremioEnDoc.Estado , ApremioEnDoc.FechaGeneracion , 
                    ApremioEnDoc.FechaEntrega
                    FROM  ApremioRelacion INNER JOIN
                    ApremioEnDoc ON ApremioRelacion.Id1erRequerimiento = ApremioEnDoc.IdDocumento
                    WHERE (ApremioEnDoc.Identidad LIKE ?) AND (ApremioEnDoc.TipoDoc = 1)
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (dni,))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def otener_info_2do_req_by_dni(self, dni):
        query = """SELECT        ApremioRelacion.IdDocumento , ApremioRelacion.Id1erRequerimiento , ApremioRelacion.TipoDoc , ApremioEnDoc.Estado , 
                        ApremioEnDoc.FechaGeneracion , ApremioEnDoc.FechaEntrega 
                        FROM            ApremioRelacion INNER JOIN
                        ApremioEnDoc ON ApremioRelacion.IdDocumento = ApremioEnDoc.IdDocumento
                        WHERE        (ApremioEnDoc.Identidad LIKE ?) AND (ApremioEnDoc.TipoDoc = 2)
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (dni,))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def otener_info_cerificacion_by_dni(self, dni):
        query = """SELECT        ApremioRelacion.IdDocumento , ApremioRelacion.Id1erRequerimiento , ApremioRelacion.TipoDoc, ApremioEnDoc.Estado , 
                    ApremioEnDoc.FechaGeneracion , ApremioEnDoc.FechaEntrega 
                    FROM            ApremioRelacion INNER JOIN
                    ApremioEnDoc ON ApremioRelacion.IdDocumento = ApremioEnDoc.IdDocumento
                    WHERE        (ApremioEnDoc.Identidad LIKE ?) AND (ApremioRelacion.TipoDoc = 3)
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (dni,))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]
