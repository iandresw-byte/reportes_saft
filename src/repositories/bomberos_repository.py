class BomberosRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_pagos_bomberos_detallado_sami(self, fecha_inicio, fecha_fin):
        query = """
            SELECT c.DNI, c.Pnombre, c.SNombre, c.PApellido, c.SApellido,
            CAST(SUM(CASE WHEN rd.ctaingreso LIKE '152190206%' THEN rd.valorunitrecibodet + rd.descto + rd.desctoamni ELSE 0 END) AS FLOAT) AS saldo,
            CAST(SUM(CASE WHEN rd.ctaingreso LIKE '152199606%' THEN rd.valorunitrecibodet + rd.descto + rd.desctoamni ELSE 0 END) AS FLOAT)  AS recargos,
            CAST(SUM(CASE WHEN rd.ctaingreso LIKE '152199706%' THEN rd.valorunitrecibodet + rd.descto + rd.desctoamni ELSE 0 END) AS FLOAT)  AS intereses,
            CAST(SUM(CASE WHEN rd.ctaingreso LIKE '152199806%' THEN rd.valorunitrecibodet + rd.descto + rd.desctoamni ELSE 0 END) AS FLOAT)  AS recuperacion,
            r.NumRecibo
            FROM FC_03 AS c INNER JOIN
            F_03 AS r ON c.DNI = r.DNI INNER JOIN
            F_04 AS rd ON r.NumRecibo = rd.NumRecibo
            WHERE (r.FechaRecibo BETWEEN ? AND ?) AND (r.ReciboAnulado = 0) AND (SUBSTRING(rd.CtaIngreso, 1, 9) IN ('152190206', '152199606', '152199706', '152199806'))
            GROUP BY c.DNI, c.Pnombre, c.SNombre, c.PApellido, c.SApellido, r.NumRecibo
            ORDER BY c.DNI
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_inicio, fecha_fin))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_pagos_bomberos_detallado_gobernacion(self, fecha_inicio, fecha_fin):
        query = """
                SELECT        c.DNI, c.Pnombre, c.SNombre, c.PApellido, c.SApellido, CAST(SUM(CASE WHEN rd.ctaingreso LIKE '11111806%' THEN rd.valorunitrecibodet + rd.descto + rd.desctoamni ELSE 0 END) AS FLOAT) AS saldo, 
                CAST(SUM(CASE WHEN rd.ctaingreso LIKE '11212305%' THEN rd.valorunitrecibodet + rd.descto + rd.desctoamni ELSE 0 END) AS FLOAT) AS recuperacion, CAST(SUM(rd.Recargo) AS FLOAT) AS recargo, CAST(SUM(rd.Interes) 
                AS FLOAT) AS interes, r.NumRecibo
                FROM            FC_03 AS c INNER JOIN
                F_03 AS r ON c.DNI = r.DNI INNER JOIN
                F_04 AS rd ON r.NumRecibo = rd.NumRecibo
                WHERE        (SUBSTRING(rd.CtaIngreso, 1, 8) IN ('11111806', '11212305')) AND (r.FechaRecibo BETWEEN ? AND ?) AND (r.ReciboAnulado = 0)
                GROUP BY c.DNI, c.Pnombre, c.SNombre, c.PApellido, c.SApellido, r.NumRecibo
                ORDER BY c.DNI
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_inicio, fecha_fin))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_pagos_bomberos_cuenta_sami(self, fecha_inicio, fecha_fin):
        query = """
            SELECT CuentaIngreso_A.NombreCtaIngreso, rd.CtaIngreso, CAST(SUM(rd.ValorUnitReciboDet + rd.Descto + rd.DesctoAmni) AS FLOAT) AS Saldo
            FROM F_03 AS r INNER JOIN
            F_04 AS rd ON r.NumRecibo = rd.NumRecibo INNER JOIN
            CuentaIngreso_A ON rd.CtaIngreso = CuentaIngreso_A.CtaIngreso AND YEAR(r.FechaRecibo) = CuentaIngreso_A.Anio
            WHERE (r.FechaRecibo BETWEEN ? AND ?) AND (r.ReciboAnulado = 0) AND (SUBSTRING(rd.CtaIngreso, 1, 9) IN ('152190206', '152199806', '152199706', '152199606'))
            GROUP BY CuentaIngreso_A.NombreCtaIngreso, rd.CtaIngreso
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_inicio, fecha_fin))
            rows = cur.fetchall()
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]
