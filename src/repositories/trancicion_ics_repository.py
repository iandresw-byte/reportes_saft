class TrancicionICSRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_ics_urbano(self, codAldea: str):
        query = """
            SELECT COUNT(DNI) AS Total FROM FC_03 WHERE (Tipo = 1) AND (CodAldea = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_ics_rural(self, codAldea: str):
        query = """
           SELECT COUNT(DNI) AS Total FROM FC_03 WHERE (Tipo = 1) AND (CodAldea <> ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_isc_rural_activos(self, codAldea: str, anio: str):
        anio = str(anio)[:4]
        query = """
            SELECT COUNT(DISTINCT F_01.DNI) AS Total
            FROM F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI
            WHERE  (FC_03.Tipo = 1) and (FC_03.CodAldea <> ?)  AND (F_01.AvPgEstado = 2) AND (year(F_01.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_ics_urbano_activos(self, codAldea: str, anio: str):
        anio = str(anio)[:4]
        query = """
            SELECT COUNT(DISTINCT F_01.DNI) AS Total
            FROM F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI
            WHERE   (FC_03.Tipo = 1)  AND (FC_03.CodAldea = ?)  AND (F_01.AvPgEstado = 2) AND (year(F_01.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))
# DETALLE DE INDUSTRIA Y COMERCIO

    def obtener_ics_urbano_detalle(self, codAldea: str):
        query = """
            SELECT FC_03.DNI, FC_03.Pnombre, CuentaIngreso_A.NombreCtaIngreso, FC_03.Direccion
            FROM FC_03 INNER JOIN
            CuentaIngreso_A ON FC_03.UltPeriodoFact = CuentaIngreso_A.Anio AND FC_03.CodProfesion = CuentaIngreso_A.CtaIngreso
            WHERE  (FC_03.Tipo = 1) AND (FC_03.CodAldea = ?)
            GROUP BY FC_03.DNI, FC_03.Pnombre, CuentaIngreso_A.NombreCtaIngreso, FC_03.Direccion
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_ics_rural_detalle(self, codAldea: str):
        query = """
            SELECT FC_03.DNI, FC_03.Pnombre, CuentaIngreso_A.NombreCtaIngreso, FC_03.Direccion
            FROM FC_03 INNER JOIN
            CuentaIngreso_A ON FC_03.UltPeriodoFact = CuentaIngreso_A.Anio AND FC_03.CodProfesion = CuentaIngreso_A.CtaIngreso
            WHERE  (FC_03.Tipo = 1) AND (FC_03.CodAldea <> ?)
            GROUP BY FC_03.DNI, FC_03.Pnombre, CuentaIngreso_A.NombreCtaIngreso, FC_03.Direccion
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_isc_rural_activos_detalle(self, codAldea: str, anio: str):
        anio = str(anio)[:4]
        query = """
            SELECT FC_03.DNI, FC_03.Pnombre, CuentaIngreso_A.NombreCtaIngreso, FC_03.Direccion, FC_03.UltPeriodoFact
            FROM F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
            CuentaIngreso_A ON FC_03.UltPeriodoFact = CuentaIngreso_A.Anio AND FC_03.CodProfesion = CuentaIngreso_A.CtaIngreso
            WHERE (FC_03.Tipo = 1) AND (FC_03.CodAldea <> ?) AND (F_01.AvPgEstado = 2) AND (year(F_01.FechaVenceAvPg) = ?)
            GROUP BY FC_03.DNI, FC_03.Pnombre, CuentaIngreso_A.NombreCtaIngreso, FC_03.Direccion, FC_03.UltPeriodoFact
           """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, anio))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_isc_urbano_activos_detalle(self, codAldea: str, anio: str):
        anio = str(anio)[:4]
        query = """
            SELECT FC_03.DNI, FC_03.Pnombre, CuentaIngreso_A.NombreCtaIngreso, FC_03.Direccion, FC_03.UltPeriodoFact
            FROM F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
            CuentaIngreso_A ON FC_03.UltPeriodoFact = CuentaIngreso_A.Anio AND FC_03.CodProfesion = CuentaIngreso_A.CtaIngreso
            WHERE (FC_03.Tipo = 1) AND (FC_03.CodAldea = ?) AND (F_01.AvPgEstado = 2) AND (year(F_01.FechaVenceAvPg) = ?)
            GROUP BY FC_03.DNI, FC_03.Pnombre, CuentaIngreso_A.NombreCtaIngreso, FC_03.Direccion, FC_03.UltPeriodoFact
           """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, anio))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]
