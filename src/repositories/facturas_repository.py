class FacturasRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_mora_bi(self, cta_bi: str):
        query = """
            SELECT CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT) AS valor
                FROM F_01 INNER JOIN
                F_02 ON F_01.NumAvPg = F_02.NumAvPg
                WHERE (F_01.FechaVenceAvPg < GETDATE()) AND (F_01.AvPgEstado = 1) AND (F_02.CtaIngreso = ?) AND (F_01.AvPgTipoImpuesto = 1)
            GROUP BY F_02.CtaIngreso
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_bi,))
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_mora_ip(self, cta_ip: str):
        query = """
            SELECT CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT) AS valor
                FROM F_01 INNER JOIN
                F_02 ON F_01.NumAvPg = F_02.NumAvPg
                WHERE (F_01.FechaVenceAvPg < GETDATE()) AND (F_01.AvPgEstado = 1) AND (F_02.CtaIngreso = ?) 
            GROUP BY F_02.CtaIngreso
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_ip,))
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_int_rec_ip(self, cta_ip: str):
        query = """
            SELECT CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT) AS valor
                FROM F_01 INNER JOIN
                F_02 ON F_01.NumAvPg = F_02.NumAvPg
                WHERE (F_01.FechaVenceAvPg < GETDATE()) AND (F_01.AvPgEstado = 1) AND (F_02.CtaIngreso = ?) AND (F_01.AvPgTipoImpuesto = 4)
            GROUP BY F_02.CtaIngreso
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_ip,))
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_mora_ics(self, cta_ics: str):
        query = """
                SELECT F_02.CtaIngreso, CuentaIngreso_A.NombreCtaIngreso, CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT) AS valor
                FROM F_02 INNER JOIN
                CuentaIngreso_A ON F_02.CtaIngreso = CuentaIngreso_A.CtaIngreso INNER JOIN
                F_01 ON F_02.NumAvPg = F_01.NumAvPg AND CuentaIngreso_A.Anio = DATEPART(year, F_01.FechaEmAvPg)
                WHERE (SUBSTRING(F_02.CtaIngreso, 1, 6) = ?) AND (F_01.AvPgEstado = 1) and FechaVenceAvPg < getdate()
                GROUP BY F_02.CtaIngreso, CuentaIngreso_A.NombreCtaIngreso 
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_ics,))
            rows = cur.fetchall()

            if not rows:
                return []

            columns = [column[0] for column in cur.description]

            # ✅ Convertir a lista de diccionarios
            resultados = [dict(zip(columns, row)) for row in rows]

            return resultados

    def obtener_interes_ics(self, cta_intres_ics: str):
        query = """
                SELECT F_02.CtaIngreso, CuentaIngreso_A.NombreCtaIngreso, CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT) AS valor
                FROM F_02 INNER JOIN
                CuentaIngreso_A ON F_02.CtaIngreso = CuentaIngreso_A.CtaIngreso INNER JOIN
                F_01 ON F_02.NumAvPg = F_01.NumAvPg AND CuentaIngreso_A.Anio = DATEPART(year, F_01.FechaEmAvPg)
                WHERE (F_02.CtaIngreso = ?) AND (F_01.AvPgEstado = 1)  AND (F_01.AvPgTipoImpuesto in (2,3))
                GROUP BY F_02.CtaIngreso, CuentaIngreso_A.NombreCtaIngreso
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_intres_ics,))
            rows = cur.fetchall()

            if not rows:
                return []

            columns = [column[0] for column in cur.description]

            # ✅ Convertir a lista de diccionarios
            resultados = [dict(zip(columns, row)) for row in rows]

            return resultados

    def obtener_tasas_ics(self, cta_intres_ics: str):
        query = """
                SELECT F_02.CtaIngreso, CuentaIngreso_A.NombreCtaIngreso, CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT) AS valor
                FROM F_02 INNER JOIN
                CuentaIngreso_A ON F_02.CtaIngreso = CuentaIngreso_A.CtaIngreso INNER JOIN
                F_01 ON F_02.NumAvPg = F_01.NumAvPg AND CuentaIngreso_A.Anio = DATEPART(year, F_01.FechaEmAvPg)
                WHERE (F_02.CtaIngreso like ?) AND (F_01.AvPgEstado = 1)
                GROUP BY F_02.CtaIngreso, CuentaIngreso_A.NombreCtaIngreso
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (f'{cta_intres_ics}%',))
            rows = cur.fetchall()

            if not rows:
                return []

            columns = [column[0] for column in cur.description]

            # ✅ Convertir a lista de diccionarios
            resultados = [dict(zip(columns, row)) for row in rows]

            return resultados

    def obtener_mora_sp(self, cta_sp: str):
        query = """
                SELECT F_02.CtaIngreso, CuentaIngreso_A.NombreCtaIngreso, CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT) AS valor
                FROM F_02 INNER JOIN
                CuentaIngreso_A ON F_02.CtaIngreso = CuentaIngreso_A.CtaIngreso INNER JOIN
                F_01 ON F_02.NumAvPg = F_01.NumAvPg AND CuentaIngreso_A.Anio = DATEPART(year, F_01.FechaEmAvPg)
                WHERE (F_02.CtaIngreso like ?) AND (F_01.AvPgEstado = 1) and FechaVenceAvPg < getdate()
                GROUP BY F_02.CtaIngreso, CuentaIngreso_A.NombreCtaIngreso
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (f'{cta_sp}%',))
            rows = cur.fetchall()

            if not rows:
                return []

            columns = [column[0] for column in cur.description]

            # ✅ Convertir a lista de diccionarios
            resultados = [dict(zip(columns, row)) for row in rows]

            return resultados
