class TrancicionAMBRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_amb_urbano(self, codAldea: str, ctaIngreso: str):
        query = """SELECT        COUNT(DISTINCT F_01.DNI) AS Total
                    FROM            F_01 INNER JOIN
                    F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
                    FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
                    CuentaIngreso_A ON F_02.CtaIngreso = CuentaIngreso_A.CtaIngreso AND YEAR(F_01.FechaVenceAvPg) = CuentaIngreso_A.Anio
                    WHERE        (FC_03.CodAldea = ?) AND (F_02.CtaIngreso LIKE ?) AND (F_01.AvPgEstado <> 3) AND 
                    (CuentaIngreso_A.Tipo <> 3)
                    """

        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,  f'{ctaIngreso}%',))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_amb_rural(self, codAldea: str, ctaIngreso: str):
        query = """SELECT        COUNT(DISTINCT F_01.DNI) AS Total
                    FROM            F_01 INNER JOIN
                    F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
                    FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
                    CuentaIngreso_A ON F_02.CtaIngreso = CuentaIngreso_A.CtaIngreso AND YEAR(F_01.FechaVenceAvPg) = CuentaIngreso_A.Anio
                    WHERE        (FC_03.CodAldea <> ?) AND (F_02.CtaIngreso LIKE ?) AND  (F_01.AvPgEstado <> 3) AND 
                    (CuentaIngreso_A.Tipo <> 3)
                    """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,  f'{ctaIngreso}%',))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_amb_rural_activos(self, codAldea: str, anio: str, ctaIngreso: str):
        anio = str(anio)[:4]
        query = """SELECT        COUNT(DISTINCT F_01.DNI) AS Total
                    FROM            F_01 INNER JOIN
                    F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
                    FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
                    CuentaIngreso_A ON F_02.CtaIngreso = CuentaIngreso_A.CtaIngreso AND YEAR(F_01.FechaVenceAvPg) = CuentaIngreso_A.Anio
                    WHERE        (FC_03.CodAldea <> ?) AND (F_02.CtaIngreso LIKE ?) AND (F_01.AvPgEstado = 2) AND (year(F_01.FechaVenceAvPg) = ?)  AND 
                    (CuentaIngreso_A.Tipo <> 3)
                    """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, f'{ctaIngreso}%', anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_amb_urbano_activos(self, codAldea: str, anio: str, ctaIngreso: str):
        anio = str(anio)[:4]
        query = """
                    SELECT        COUNT(DISTINCT F_01.DNI) AS Total
                    FROM            F_01 INNER JOIN
                    F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
                    FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
                    CuentaIngreso_A ON F_02.CtaIngreso = CuentaIngreso_A.CtaIngreso AND YEAR(F_01.FechaVenceAvPg) = CuentaIngreso_A.Anio
                    WHERE        (FC_03.CodAldea = ?) AND (F_02.CtaIngreso LIKE ?) AND (F_01.AvPgEstado = 2) AND (year(F_01.FechaVenceAvPg) = ?)  AND 
                    (CuentaIngreso_A.Tipo <> 3)
                         """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, f'{ctaIngreso}%', anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))
# impuestos de extraccion y selectivo detalle

    def obtener_amb_urbano_detalle(self, codAldea: str, ctaIngreso: str):
        query = """
                SELECT FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido
                FROM F_01 INNER JOIN
                F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
                FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
                CuentaIngreso_A ON F_02.CtaIngreso = CuentaIngreso_A.CtaIngreso AND YEAR(F_01.FechaVenceAvPg) = CuentaIngreso_A.Anio
                WHERE  (FC_03.CodAldea = ?) AND (F_02.CtaIngreso LIKE ?) AND (F_01.AvPgEstado <> 3) AND (CuentaIngreso_A.Tipo <> 3)
                GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido
              """

        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,  f'{ctaIngreso}%',))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_amb_rural_detalle(self, codAldea: str, ctaIngreso: str):
        query = """
                SELECT FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido
                FROM F_01 INNER JOIN
                F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
                FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
                CuentaIngreso_A ON F_02.CtaIngreso = CuentaIngreso_A.CtaIngreso AND YEAR(F_01.FechaVenceAvPg) = CuentaIngreso_A.Anio
                WHERE  (FC_03.CodAldea <> ?) AND (F_02.CtaIngreso LIKE ?) AND (F_01.AvPgEstado <> 3) AND (CuentaIngreso_A.Tipo <> 3)
                GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido
            
              """

        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,  f'{ctaIngreso}%',))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_amb_rural_activos_detalle(self, codAldea: str, anio: str, ctaIngreso: str):
        anio = str(anio)[:4]
        query = """
                SELECT FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido
                FROM F_01 INNER JOIN
                F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
                FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
                CuentaIngreso_A ON F_02.CtaIngreso = CuentaIngreso_A.CtaIngreso AND YEAR(F_01.FechaVenceAvPg) = CuentaIngreso_A.Anio
                WHERE  (FC_03.CodAldea <> ?) AND (F_02.CtaIngreso LIKE ?) AND (F_01.AvPgEstado = 2) AND (CuentaIngreso_A.Tipo <> 3) and (year(F_01.FechaVenceAvPg)  = ?)
                GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido
            """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, f'{ctaIngreso}%', anio))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_amb_urbano_activos_detalle(self, codAldea: str, anio: str, ctaIngreso: str):
        anio = str(anio)[:4]
        query = """SELECT FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido
                FROM F_01 INNER JOIN
                F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
                FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
                CuentaIngreso_A ON F_02.CtaIngreso = CuentaIngreso_A.CtaIngreso AND YEAR(F_01.FechaVenceAvPg) = CuentaIngreso_A.Anio
                WHERE  (FC_03.CodAldea = ?) AND (F_02.CtaIngreso LIKE ?) AND (F_01.AvPgEstado = 2) AND (CuentaIngreso_A.Tipo <> 3) and (year(F_01.FechaVenceAvPg) = ?)
                GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido
             """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, f'{ctaIngreso}%', anio))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]
