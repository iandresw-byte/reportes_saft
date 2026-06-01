class PrescripcionesRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtenter_analis_prescripcion(self,  tipo_impuesto: int):
        query = """
            DECLARE @FechaLimite DATE = DATEADD(YEAR, -5, CAST(GETDATE() AS DATE));
            SELECT e.DNI, FC_03.Pnombre + ' ' + FC_03.SNombre + ' ' + FC_03.PApellido + ' ' + FC_03.SApellido AS Nombre, '2020-12-16' AS Expr1, 
            CAST(SUM(CASE WHEN e.FechaVenceAvPg < '20201216' THEN d .ValorUnitAvPgDet ELSE 0 END) AS FLOAT ) AS PRESCRITO, CAST(SUM(CASE WHEN e.FechaVenceAvPg >= '20201216' THEN d .ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS RECUPERABLE, 
            MIN(e.FechaVenceAvPg) AS FechaInicio, MAX(e.FechaVenceAvPg) AS FechaFinal, CAST(SUM(d.ValorUnitAvPgDet) AS FLOAT) AS SALDO
            FROM F_01 AS e INNER JOIN
            F_02 AS d ON e.NumAvPg = d.NumAvPg INNER JOIN
            FC_03 ON e.DNI = FC_03.DNI
            WHERE (e.AvPgTipoImpuesto = ?)
            GROUP BY e.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (tipo_impuesto,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]
