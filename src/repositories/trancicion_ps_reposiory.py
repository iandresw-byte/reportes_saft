class TrancicionSPRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_sp_gob_inicio(self, cta_sp: str, anio: str):
        query = """
            SELECT SUBSTRING(F_02.CtaIngreso, 1, 8) AS Cuenta, COUNT(DISTINCT F_01.DNI) AS Total
            FROM F_02 INNER JOIN
            F_01 ON F_02.NumAvPg = F_01.NumAvPg
            WHERE (SUBSTRING(F_02.CtaIngreso, 1, 6) IN (?)) AND (F_01.FechaVenceAvPg < ?)
            GROUP BY SUBSTRING(F_02.CtaIngreso, 1, 8)
            ORDER BY Cuenta
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_sp, anio,))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def obtener_sp_sami_inicio(self, anio: int, cta_sp: str):
        query = """
                SELECT SUBSTRING(F_02.CtaIngreso, 1, 9) AS Cuenta, COUNT(DISTINCT F_01.DNI) AS Total
                FROM F_02 INNER JOIN
                F_01 ON F_02.NumAvPg = F_01.NumAvPg
                WHERE (DATEPART(year, F_01.FechaVenceAvPg) > ?) AND (SUBSTRING(F_02.CtaIngreso, 1, 7) IN (?))
                GROUP BY SUBSTRING(F_02.CtaIngreso, 1, 9)
                ORDER BY Cuenta
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (anio, cta_sp))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def obtener_sp_gob_final(self, cta_sp: str):
        query = """
            SELECT SUBSTRING(F_02.CtaIngreso, 1, 8) AS Cuenta, COUNT(DISTINCT F_01.DNI) AS Total
            FROM F_02 INNER JOIN
            F_01 ON F_02.NumAvPg = F_01.NumAvPg
            WHERE (SUBSTRING(F_02.CtaIngreso, 1, 6) IN (?)) 
            GROUP BY SUBSTRING(F_02.CtaIngreso, 1, 8)
            ORDER BY Cuenta
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_sp,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def obtener_sp_sami_final(self, cta_sp: str):
        query = """
                SELECT SUBSTRING(F_02.CtaIngreso, 1, 9) AS Cuenta, COUNT(DISTINCT F_01.DNI) AS Total
                FROM F_02 INNER JOIN
                F_01 ON F_02.NumAvPg = F_01.NumAvPg
                WHERE  (SUBSTRING(F_02.CtaIngreso, 1, 7) IN (?))
                GROUP BY SUBSTRING(F_02.CtaIngreso, 1, 9)
                ORDER BY Cuenta
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_sp,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]


# DETALLE SERVICIOS PUBLICOS


    def obtener_sp_gob_inicio_detalle(self, cta_sp: str, anio: str):
        query = """
            SELECT F_01.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.Direccion
            FROM  F_02 INNER JOIN
            F_01 ON F_02.NumAvPg = F_01.NumAvPg INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI
            WHERE ( F_01.FechaVenceAvPg < ?) AND (SUBSTRING(F_02.CtaIngreso, 1, 8) IN (?))
            GROUP BY  F_01.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.Direccion
            ORDER BY F_01.DNI
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_sp, anio,))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def obtener_sp_sami_inicio_detalle(self, anio: str, cta_sp: str):
        query = """
            SELECT FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.sApellido, FC_03.Direccion
            FROM  F_02 INNER JOIN
            F_01 ON F_02.NumAvPg = F_01.NumAvPg INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI
            WHERE  (F_01.FechaVenceAvPg  < ?) AND (SUBSTRING(F_02.CtaIngreso, 1, 9) IN (?))
            GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.sApellido, FC_03.Direccion
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (anio, cta_sp))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def obtener_sp_gob_final_detalle(self, cta_sp: str):
        query = """
            SELECT F_01.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.Direccion
            FROM  F_02 INNER JOIN
            F_01 ON F_02.NumAvPg = F_01.NumAvPg INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI
            WHERE  (SUBSTRING(F_02.CtaIngreso, 1, 8) IN (?))
            GROUP BY  F_01.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.Direccion
            ORDER BY F_01.DNI
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_sp))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def obtener_sp_sami_final_detalle(self,  cta_sp: str):
        query = """
            SELECT FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.Direccion
            FROM  F_02 INNER JOIN
            F_01 ON F_02.NumAvPg = F_01.NumAvPg INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI
            WHERE   (SUBSTRING(F_02.CtaIngreso, 1, 9) IN (?))
            GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.Direccion
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_sp))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]
