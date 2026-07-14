class PlanesPagoRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_planes_pago(self, identidad: str, num_plan_pago: int):
        query = """
                    """
        with self.conexion.cursor() as cur:
            cur.execute(query, (identidad, num_plan_pago))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def obtener_facturas_en_plan_pago(self, num_plan_pago):
        query = """
                    DECLARE @NUM_PP INT = ?;
                    SELECT  
                    CAST(F_01.NumAvPg AS int) AS NumAvPg, 
                    CAST(SUM(F_02.ValorUnitAvPgDet) AS float) AS valorFacturaenPP
                    FROM F_01 INNER JOIN F_02 ON F_01.NumAvPg = F_02.NumAvPg
                    WHERE (F_01.NumAvPg IN (SELECT NumAvPg FROM PlanPagoDetalle WHERE (SeqPP = @NUM_PP)))
                    GROUP BY F_01.NumAvPg
                    ORDER BY F_01.NumAvPg;
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_plan_pago,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def obtener_cuotas_plan_pago(self, num_plan_pago: str):
        query = """SELECT  F_01.NumAvPg, 
                    CAST(SUM(F_02.ValorUnitAvPgDet) AS float) AS ValorCouta,
                    CAST(DATEDIFF(MONTH, F_01.FechaVenceAvPg, GETDATE()) as Int) AS MesesVencidos,
                    F_01.AvPgEstado
                    FROM F_01 INNER JOIN  F_02 ON F_01.NumAvPg = F_02.NumAvPg
                    WHERE (F_01.NumAvPg IN (SELECT NumAvPg FROM PlanPagoFactura WHERE (SeqPP = ?)))
                    GROUP BY F_01.NumAvPg, F_01.AvPgEstado, F_01.FechaVenceAvPg
                    ORDER BY F_01.NumAvPg;
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_plan_pago,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]



    def reversar_factura_en_pp(self, num_plan_pago, num_avp_pg):
        query = """
                UPDATE F_01
                SET AvPgEstado = 1
                WHERE (NumAvPg IN (SELECT NumAvPg FROM PlanPagoDetalle WHERE (SeqPP = ?))) AND (AvPgEstado = 6) AND (NumAvPg =?)
            """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_plan_pago,num_avp_pg,))

    def anular_cuota_pp(self, num_plan_pago):
        query = """
                UPDATE F_01
                SET AvPgEstado = 3
                WHERE (NumAvPg IN (SELECT NumAvPg FROM PlanPagoFactura WHERE (SeqPP = ?))) AND (AvPgEstado = 1)
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_plan_pago,))
    
    def modificar_ultima_factura_plan_pago(self,nuevo_valor, num_avpg, cta_ingreso):
        query = """
                UPDATE F_02
                SET ValorUnitAvPgDet = ?
                WHERE NumAvPg = ? AND CtaIngreso = ?
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (nuevo_valor, num_avpg, cta_ingreso,))
    
    def get_factura_detalle(self,num_avpg):
        query = """
                SELECT NumAvPg, CtaIngreso, 
                CAST((ValorUnitAvPgDet * CantAvpgDet) as Float)  as ValorUnitAvPgDet FROM F_02
                WHERE NumAvPg = ? and ctaingreso not in ( '11212701', '11212703','11212702')
                """
        with self.conexion.cursor() as cur:
            rows = cur.execute(query, (num_avpg,))
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]
    
    def anular_num_plan(self, num_plan_pago):
        query = """
                UPDATE       PlanPago
                SET                EstadoPP = 1
                WHERE        (SeqPP = ?)
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_plan_pago,))


    
    def get_data_plan_pago(self, num_plan_pago):
        query = """
    SELECT PlanPago.SeqPP, 
        PlanPago.Identidad, 
        CAST(PlanPago.FechaInicioPP  AS Date) AS FechaInicioPP,
        CAST(PlanPago.NumCuotasPP  AS Int) AS NumCuotasPP,
        CAST(PlanPago.ValorCuotaPP  AS FLOAT) AS ValorCuotaPP,
        CAST(PlanPago.TotalPagadoPP  AS FLOAT) AS TotalPagadoPP, 
        CAST(PlanPago.MontoPP  AS FLOAT) AS MontoPP, 
        CAST(PlanPago.EstadoPP  AS int) AS EstadoPP, 
        FC_03.PNombre, FC_03.SNombre,  FC_03.PApellido, FC_03.SApellido, 
        FC_03.Direccion
    FROM PlanPago INNER JOIN
        FC_03 ON PlanPago.Identidad = FC_03.DNI
    WHERE   (PlanPago.SeqPP = ?)
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_plan_pago,))
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    
    
    


   