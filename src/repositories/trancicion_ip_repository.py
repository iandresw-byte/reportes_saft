class TrancicionIPRepository:
    def __init__(self, conexion):
        self.conexion = conexion
    # DECLARADO

    def obtener_ip_urbano(self, codAldea: str):
        query = """
            SELECT COUNT(DISTINCT F_01.DNI) AS Total
            FROM F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI
            WHERE (F_01.AvPgTipoImpuesto = 4) AND (FC_03.CodAldea = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_ip_rural(self, codAldea: str):
        query = """
            SELECT COUNT(DISTINCT F_01.DNI) AS Total
            FROM F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI
            WHERE (F_01.AvPgTipoImpuesto = 4) AND (FC_03.CodAldea <> ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_ip_rural_activos(self, codAldea: str, anio: str):
        anio = str(anio)[:4]

        query = """
            SELECT COUNT(DISTINCT F_01.DNI) AS Total
            FROM F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI
            WHERE (F_01.AvPgTipoImpuesto = 4) AND (FC_03.CodAldea <> ?)  AND (F_01.AvPgEstado = 2) AND (year(F_01.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_ip_urbano_activos(self, codAldea: str, anio: str):
        anio = str(anio)[:4]
        query = """
            SELECT COUNT(DISTINCT F_01.DNI) AS Total
            FROM F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI
            WHERE (F_01.AvPgTipoImpuesto = 4) AND (FC_03.CodAldea = ?)  AND (F_01.AvPgEstado = 2) AND (year(F_01.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    # OTRAS TASAS
    def obtener_ip_urbano_ot(self, CodAldea: str,  cta_ip: str):
        query = """
            SELECT COUNT(DISTINCT F_01.DNI) AS Total
            FROM  F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
            F_02 ON F_01.NumAvPg = F_02.NumAvPg
            WHERE (F_01.AvPgTipoImpuesto <> 4) AND (FC_03.CodAldea = ?) AND (F_02.CtaIngreso LIKE ?) AND (F_01.DNI NOT IN
            (SELECT F_01_1.DNI
            FROM  F_01 AS F_01_1 INNER JOIN
            FC_03 AS FC_03_1 ON F_01_1.DNI = FC_03_1.DNI
            WHERE (F_01_1.AvPgTipoImpuesto = 4)
            GROUP BY F_01_1.DNI))
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (CodAldea, cta_ip,))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_ip_rural_ot(self, CodAldea: str,  cta_ip: str):
        query = """
          SELECT COUNT(DISTINCT F_01.DNI) AS Total
            FROM  F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
            F_02 ON F_01.NumAvPg = F_02.NumAvPg
            WHERE (F_01.AvPgTipoImpuesto <> 4) AND (FC_03.CodAldea <> ?) AND (F_02.CtaIngreso LIKE ?) AND (F_01.DNI NOT IN
            (SELECT F_01_1.DNI
            FROM  F_01 AS F_01_1 INNER JOIN
            FC_03 AS FC_03_1 ON F_01_1.DNI = FC_03_1.DNI
            WHERE (F_01_1.AvPgTipoImpuesto = 4)
            GROUP BY F_01_1.DNI))
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (CodAldea, cta_ip,))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_ip_rural_activos_ot(self, codAldea: str,  cta_ip: str, anio: str):
        anio = str(anio)[:4]
        query = """
            SELECT COUNT(DISTINCT F_01.DNI) AS Total
            FROM  F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
            F_02 ON F_01.NumAvPg = F_02.NumAvPg
            WHERE (F_01.AvPgTipoImpuesto <> 4) AND (FC_03.CodAldea <> ?) AND (F_02.CtaIngreso LIKE ?) AND (F_01.DNI NOT IN
            (SELECT F_01_1.DNI
            FROM  F_01 AS F_01_1 INNER JOIN
            FC_03 AS FC_03_1 ON F_01_1.DNI = FC_03_1.DNI
            WHERE (F_01_1.AvPgTipoImpuesto = 4)
            GROUP BY F_01_1.DNI)) AND (F_01.AvPgEstado = 2) AND (year(F_01.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, cta_ip, anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_ip_urbano_activos_ot(self, codAldea: str,  cta_ip: str, anio: str):
        anio = str(anio)[:4]
        query = """
            SELECT COUNT(DISTINCT F_01.DNI) AS Total
            FROM  F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
            F_02 ON F_01.NumAvPg = F_02.NumAvPg
            WHERE (F_01.AvPgTipoImpuesto <> 4) AND (FC_03.CodAldea = ?) AND (F_02.CtaIngreso LIKE ?) AND (F_01.DNI NOT IN
            (SELECT F_01_1.DNI
            FROM  F_01 AS F_01_1 INNER JOIN
            FC_03 AS FC_03_1 ON F_01_1.DNI = FC_03_1.DNI
            WHERE (F_01_1.AvPgTipoImpuesto = 4)
            GROUP BY F_01_1.DNI))  AND (F_01.AvPgEstado = 2) AND (year(F_01.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, cta_ip, anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    # DETALLE DECLRADO
    def obtener_ip_urbano_detalle(self, codAldea: str):
        query = """
            SELECT FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.UltPeriodoFact
            FROM  F_01 INNER JOIN FC_03 ON F_01.DNI = FC_03.DNI
            WHERE  (F_01.AvPgTipoImpuesto = 4) AND (FC_03.CodAldea = ?)
            GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.UltPeriodoFact
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_ip_rural_detalle(self, codAldea: str):
        query = """
            SELECT FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.UltPeriodoFact
            FROM  F_01 INNER JOIN FC_03 ON F_01.DNI = FC_03.DNI
            WHERE  (F_01.AvPgTipoImpuesto = 4) AND (FC_03.CodAldea <> ?)
            GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.UltPeriodoFact
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_ip_rural_activos_detalle(self, codAldea: str, anio: str):
        anio = str(anio)[:4]
        query = """
            SELECT FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.UltPeriodoFact
            FROM F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI
            WHERE (F_01.AvPgTipoImpuesto = 4) AND (FC_03.CodAldea <> ?)  AND (F_01.AvPgEstado = 2) AND (year(F_01.FechaVenceAvPg) = ?)
            GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.UltPeriodoFact
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, anio))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_ip_urbano_activos_detalle(self, codAldea: str, anio: str):
        anio = str(anio)[:4]
        query = """
            SELECT FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.UltPeriodoFact
            FROM F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI
            WHERE (F_01.AvPgTipoImpuesto = 4) AND (FC_03.CodAldea = ?)  AND (F_01.AvPgEstado = 2) AND (year(F_01.FechaVenceAvPg) = ?)
            GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.UltPeriodoFact
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, anio))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    # DETALLE OTRAS TASAS

    def obtener_ip_urbano_ot_detalle(self, CodAldea: str,  cta_ip: str):
        query = """
                SELECT  FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.UltPeriodoFact
                FROM F_01 INNER JOIN
                FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
                F_02 ON F_01.NumAvPg = F_02.NumAvPg
                WHERE (F_01.AvPgTipoImpuesto <> 4) AND (FC_03.CodAldea = ?) AND (F_02.CtaIngreso LIKE ?) AND (F_01.DNI NOT IN
                (SELECT F_01_1.DNI FROM  F_01 AS F_01_1 INNER JOIN
                FC_03 AS FC_03_1 ON F_01_1.DNI = FC_03_1.DNI
                WHERE (F_01_1.AvPgTipoImpuesto = 4)
                GROUP BY F_01_1.DNI))
                GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.UltPeriodoFact
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (CodAldea, cta_ip,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_ip_rural_ot_detalle(self, CodAldea: str,  cta_ip: str):
        query = """
                SELECT  FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.UltPeriodoFact
                FROM F_01 INNER JOIN
                FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
                F_02 ON F_01.NumAvPg = F_02.NumAvPg
                WHERE (F_01.AvPgTipoImpuesto <> 4) AND (FC_03.CodAldea <> ?) AND (F_02.CtaIngreso LIKE ?) AND (F_01.DNI NOT IN
                (SELECT F_01_1.DNI FROM  F_01 AS F_01_1 INNER JOIN
                FC_03 AS FC_03_1 ON F_01_1.DNI = FC_03_1.DNI
                WHERE (F_01_1.AvPgTipoImpuesto = 4)
                GROUP BY F_01_1.DNI))
                GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.UltPeriodoFact
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (CodAldea, cta_ip,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_ip_rural_activos_ot_detalle(self, codAldea: str,  cta_ip: str, anio: str):
        anio = str(anio)[:4]
        query = """
            SELECT FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.UltPeriodoFact
            FROM F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
            F_02 ON F_01.NumAvPg = F_02.NumAvPg
            WHERE (F_01.AvPgTipoImpuesto <> 4) AND (FC_03.CodAldea <> ?) AND (F_02.CtaIngreso LIKE ?) AND (F_01.DNI NOT IN
            (SELECT  F_01_1.DNI
            FROM F_01 AS F_01_1 INNER JOIN
            FC_03 AS FC_03_1 ON F_01_1.DNI = FC_03_1.DNI
            WHERE (F_01_1.AvPgTipoImpuesto = 4)
            GROUP BY F_01_1.DNI)) AND (F_01.AvPgEstado = 2) AND year(F_01.FechaVenceAvPg) = ?
            GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.UltPeriodoFact
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, cta_ip, anio))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_ip_urbano_activos_ot_detalle(self, codAldea: str,  cta_ip: str, anio: str):
        anio = str(anio)[:4]
        query = """
              SELECT FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.UltPeriodoFact
            FROM F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
            F_02 ON F_01.NumAvPg = F_02.NumAvPg
            WHERE (F_01.AvPgTipoImpuesto <> 4) AND (FC_03.CodAldea = ?) AND (F_02.CtaIngreso LIKE ?) AND (F_01.DNI NOT IN
            (SELECT  F_01_1.DNI
            FROM F_01 AS F_01_1 INNER JOIN
            FC_03 AS FC_03_1 ON F_01_1.DNI = FC_03_1.DNI
            WHERE (F_01_1.AvPgTipoImpuesto = 4)
            GROUP BY F_01_1.DNI)) AND (F_01.AvPgEstado = 2) AND year(F_01.FechaVenceAvPg) = ?
            GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.UltPeriodoFact
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, cta_ip, anio))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]
