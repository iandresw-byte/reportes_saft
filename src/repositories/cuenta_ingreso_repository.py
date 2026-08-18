class CuentaIngresoRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_cuentas(self, cta_ingreso):
        query = " SELECT  TOP (1)  CtaIngreso, NombreCtaIngreso, CtaPermOP, CtaRecuperacion, Tipo, RangoR, Categoria, CtaInteres, CtaRecargos FROM CuentaIngreso_A WHERE (CtaIngreso LIKE ?) AND (Anio = DATEPART(year, GETDATE()))"
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_ingreso,))
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_cuentas_ics(self, cta_ingreso):
        query = " SELECT  CtaRecuperacion, CtaInteres, CtaRecargos FROM CuentaIngreso_A WHERE (CtaIngreso LIKE ?)  GROUP BY CtaRecuperacion, CtaInteres, CtaRecargos ORDER BY CtaRecuperacion DESC, CtaInteres, CtaRecargos"
        with self.conexion.cursor() as cur:
            cur.execute(query, (f'{cta_ingreso}%',))
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_cta_sp(self, cta_ingreso):
        query = " SELECT  CtaRecuperacion, CtaInteres, CtaRecargos FROM CuentaIngreso_A WHERE (CtaIngreso LIKE ?)  GROUP BY CtaRecuperacion, CtaInteres, CtaRecargos ORDER BY CtaRecuperacion DESC, CtaInteres, CtaRecargos"
        with self.conexion.cursor() as cur:
            cur.execute(query, (f'{cta_ingreso}%',))
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_lista_cuentas_tipo_impuesto(self, tipo:int):
            query = """

                    DECLARE @tipo AS INT = ?
                    
                    SELECT        CtaIngreso, NombreCtaIngreso, CtaRecuperacion, CtaInteres, CtaRecargos
                    FROM            CuentaIngreso_A
                    WHERE        (Tipo = @tipo) AND (CtaIngreso NOT IN
                    (SELECT        CtaRecuperacion
                    FROM            CuentaIngreso_A AS CuentaIngreso_A_1
                    WHERE        (Tipo = @tipo)
                    GROUP BY CtaRecuperacion))
                    GROUP BY CtaIngreso, NombreCtaIngreso, CtaRecuperacion, CtaInteres, CtaRecargos
                    ORDER BY CtaIngreso
            """
            with self.conexion.cursor() as cur:
                cur.execute(query, (tipo))
                rows = cur.fetchall()
                columns = [column[0] for column in cur.description]

                resultado = []
                for i, row in enumerate(rows, start=1):
                    registro = dict(zip(columns, row))
                    registro["Fila"] = i
                    resultado.append(registro)

                return resultado


    def obtener_lista_cuenta_mayor_mora(self, tipo:int|None):
            query = """
                SELECT        SUBSTRING(F_02.CtaIngreso, 1, 6) AS cta_Ingreso, CatalogoIngreso.Descripcion
                FROM            F_02 INNER JOIN
                CatalogoIngreso ON SUBSTRING(F_02.CtaIngreso, 1, 6) = CatalogoIngreso.CtaIngreso INNER JOIN
                F_01 ON F_02.NumAvPg = F_01.NumAvPg
                WHERE        (F_01.AvPgEstado = 1) AND (F_01.AvPgTipoImpuesto = 1)
                GROUP BY SUBSTRING(F_02.CtaIngreso, 1, 6), CatalogoIngreso.Descripcion
                ORDER BY cta_Ingreso
            """
            with self.conexion.cursor() as cur:
                cur.execute(query, (tipo))
                rows = cur.fetchall()
                columns = [column[0] for column in cur.description]

                resultado = []
                for i, row in enumerate(rows, start=1):
                    registro = dict(zip(columns, row))
                    registro["Fila"] = i
                    resultado.append(registro)

                return resultado