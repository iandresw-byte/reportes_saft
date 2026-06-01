class DashboardRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_valores_cards(self):
        query = """
            SELECT 
            CAST(SUM(AvPgDetalle.ValorUnitAvPgDet) AS FLOAT) AS TotalGenerado,
            COUNT(AvPgDetalle.NumAvPg) as TotalFacturas,
            CAST(SUM(CASE WHEN AvPgEnc.AvPgEstado = 1 THEN 1 ELSE 0 END) AS FLOAT) AS MoraTotalFacturas, 
            CAST(SUM(CASE WHEN AvPgEnc.AvPgEstado = 1 THEN AvPgDetalle.ValorUnitAvpgDet ELSE 0 END) AS FLOAT) AS MoraTotal, 
            CAST(SUM(CASE WHEN AvPgEnc.AvPgEstado = 2 THEN 1 ELSE 0 END) AS FLOAT) AS IngresosTotalFacturas, 
            CAST(SUM(CASE WHEN AvPgEnc.AvPgEstado = 2 THEN AvPgDetalle.ValorUnitAvpgDet ELSE 0 END) AS FLOAT) AS Ingresos,  
            CASE WHEN CAST(SUM(AvPgDetalle.ValorUnitAvpgDet) AS FLOAT) = 0 THEN 0 ELSE ROUND(SUM(CASE WHEN AvPgEnc.AvPgEstado = 1 THEN AvPgDetalle.ValorUnitAvpgDet END) * 100.0 / CAST(SUM(AvPgDetalle.ValorUnitAvpgDet) AS FLOAT), 2) END AS PorcentajeMora,
            CASE WHEN CAST(SUM(AvPgDetalle.ValorUnitAvpgDet) AS FLOAT) = 0 THEN 0 ELSE ROUND(SUM(CASE WHEN AvPgEnc.AvPgEstado = 2 THEN AvPgDetalle.ValorUnitAvpgDet END) * 100.0 / CAST(SUM(AvPgDetalle.ValorUnitAvpgDet) AS FLOAT), 2) END AS PorcentajeIngresos

            FROM AvPgDetalle INNER JOIN AvPgEnc ON AvPgDetalle.NumAvPg = AvPgEnc.NumAvPg 
            WHERE (AvPgEnc.AvPgEstado in (1,2)) AND  (AvPgEnc.FechaVenceAvPg < GETDATE())  
        """
        with self.conexion.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_valores_grafico(self):
        query = """
            SELECT 
            year(AvPgEnc.FechaVenceAvPg) as anio,
            CASE WHEN CAST(SUM(AvPgDetalle.ValorUnitAvpgDet) AS FLOAT) = 0 THEN 0 ELSE ROUND(SUM(CASE WHEN AvPgEnc.AvPgEstado = 1 THEN AvPgDetalle.ValorUnitAvpgDet END) * 100.0 / CAST(SUM(AvPgDetalle.ValorUnitAvpgDet) AS FLOAT), 2) END AS PorcentajeMora,
            CASE WHEN CAST(SUM(AvPgDetalle.ValorUnitAvpgDet) AS FLOAT) = 0 THEN 0 ELSE ROUND(SUM(CASE WHEN AvPgEnc.AvPgEstado = 2 THEN AvPgDetalle.ValorUnitAvpgDet END) * 100.0 / CAST(SUM(AvPgDetalle.ValorUnitAvpgDet) AS FLOAT), 2) END AS PorcentajeIngresos
            FROM AvPgDetalle INNER JOIN AvPgEnc ON AvPgDetalle.NumAvPg = AvPgEnc.NumAvPg 
            WHERE (AvPgEnc.AvPgEstado in (1,2)) AND  (AvPgEnc.FechaVenceAvPg < GETDATE())  
            group by year(AvPgEnc.FechaVenceAvPg)
            order by anio

        """
        with self.conexion.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

            if not rows:
                return None

            columns = [column[0] for column in cur.description]

            return [dict(zip(columns, row)) for row in rows]
