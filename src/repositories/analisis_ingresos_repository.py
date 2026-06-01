class AnalisisIngresosRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def analisis_ingresos_anio_act_anio_ant(self, anio: int):
        anio_inicio = int(anio)-1
        anio_final = int(anio)
        fecha_inicio = f"{anio_inicio}0101"
        fecha_final = f"{anio_final}1231"

        parms = (anio_inicio, anio_final, anio_inicio, anio_final, anio_inicio, anio_final, anio_inicio, anio_final, anio_inicio, anio_final, anio_inicio, anio_final, anio_inicio,
                 anio_final, anio_inicio, anio_final, anio_inicio, anio_final, anio_inicio, anio_final, anio_inicio, anio_final, anio_inicio, anio_final, fecha_inicio, fecha_final)
        query = f"""
            SELECT 
            substring(F_04.CtaIngreso,1,8) as cta,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 1 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS enero_ant,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 1 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS enero_act,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 2 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS febrero_ant, 
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 2 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS febrero_act, 
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 3 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS marzo_ant,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 3 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS marzo_act,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 4 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS abril_ant,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 4 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS abril_act,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 5 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS mayo_ant,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 5 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS mayo_act,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 6 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS junio_ant,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 6 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS junio_act,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 7 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS julio_ant, 
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 7 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS julio_act, 
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 8 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS agosto_ant, 
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 8 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS agosto_act,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 9 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS septiembre_ant,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 9 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS septiembre_act,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 10 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS octubre_ant,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 10 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS octubre_act,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 11 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS noviembre_ant,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 11 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS noviembre_act,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 12 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS diciembre_ant,
            CAST(SUM(CASE WHEN month(F_03.FechaRecibo) = 12 and year(F_03.FechaRecibo) = ? THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS diciembre_act
                FROM F_04 INNER JOIN F_03 ON F_04.NumRecibo = F_03.NumRecibo 
                WHERE (F_03.ReciboAnulado = 'False') AND  (F_03.FechaRecibo BETWEEN ? AND ?)  
                group by substring(F_04.CtaIngreso,1,8)
                order by cta
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, parms)
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]
