from src.models.declaracion_ip import DeclaraImpInd
from datetime import datetime


class FinalizarPagosIPRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def get_recibo(self, num_recibo):
        query = """
                SELECT        F_03.NumRecibo, F_03.FechaRecibo, FC_03.DNI, FC_03.Pnombre, F_04.NumFactura, CAST(SUM(F_04.ValorUnitReciboDet) AS FLOAT) AS monto, F_04.CtaIngreso
                FROM F_03 INNER JOIN
                F_04 ON F_03.NumRecibo = F_04.NumRecibo INNER JOIN
                FC_03 ON F_03.DNI = FC_03.DNI
                WHERE (F_03.NumRecibo = ?)
                GROUP BY F_03.DNI, F_03.DescRecibo, F_03.NumRecibo, F_03.SeqRecibo, F_03.NumFactura, F_03.CreadoPor, F_03.FechaCreado, F_03.ModificadoPor, F_03.FechaModificado, F_03.CtaBanco, F_03.NoCai, F_03.POS, F_03.Control,
                F_03.Hora, F_03.UsuarioAplico, F_03.EfecTarjeDepo, F_03.FechaRecibo, FC_03.DNI, FC_03.Pnombre, F_04.NumFactura, F_04.CtaIngreso"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_recibo,))
            rows = cur.fetchall()

            return rows

    def existe_pago(self, num_recibo):
        query = """ SELECT  COUNT(*) AS totalPagadsos FROM DeclaraNat WHERE (NumRecibo = ?)"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_recibo,))
            row = cur.fetchone()[0] > 0
            return row

    def get_ult_cod_decracion(self):
        query = """SELECT COUNT(*) AS NumDecraracion FROM DeclaraImpInd"""
        with self.conexion.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            if not row:
                return None
            return row[0]+1

    def crear_declaracion(self, data: DeclaraImpInd):
        fecha = data.FechaPresenta.strftime('%Y%m%d')
        data_insert = [data.Identidad, fecha, data.PeriodoDeclara, data.IngNoGrabados,
                       data.HonorariosProf, data.IngAlquileres, data.OtrosIngresos, data.Retencion,
                       data.Impuesto,  data.NroFactura, fecha,  fecha, data.MontoPagado,
                       data.CodDeclaraIP,  data.EstadoDeclaraIP, data.IngSueldos, data.Descuento,
                       data.MultaDeclaraTardeIP, data.RecMoraIP, data.RecSobreSaldoIP,
                       ]

        query = """
                  INSERT INTO DeclaraImpInd
                  (Identidad, FechaPresenta, PeriodoDeclara, IngNoGrabados, HonorariosProf,
                   IngAlquileres, OtrosIngresos, Retencion, Impuesto, NroFactura, FechaPagoIP,
                    FechaFacturadoIP, MontoPagado, CodDeclaraIP, EstadoDeclaraIP,
                  IngSueldos, Descuento, MultaDeclaraTardeIP, RecMoraIP, RecSobreSaldoIP)
                  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """
        with self.conexion.cursor() as cur:
            cur.execute(query, data_insert)

    def insertar_declaracion_natural_empresa(self, data):
        if isinstance(data.Fecha, str):
            fecha_formateada = datetime.strptime(
                data.Fecha, "%d/%m/%Y").strftime("%Y%m%d")
        else:
            fecha_formateada = data.Fecha.strftime("%Y%m%d")

        if isinstance(data.FechaPresenta, str):
            fecha_presenta = datetime.strptime(
                data.FechaPresenta, "%d/%m/%Y").strftime("%Y%m%d")
        else:
            fecha_presenta = data.FechaPresenta.strftime("%Y%m%d")

        data_insert = [
            data.Empresa,
            data.Identidad,
            data.Ingreso,
            data.Impuesto,
            data.Multa,
            data.Interes,
            data.Recargo,
            data.Descuento,
            data.Total,
            fecha_formateada,
            data.NumRecibo,
            data.AnioDeclara,
            fecha_presenta,
            data.UsuarioCrea,
            data.CodDeclaraIP,
            data.NumAvPg,
            data.Tasas,
            data.RTM
        ]
        query = """
        INSERT INTO DeclaraNat (Empresa, Identidad, Ingreso, Impuesto, Multa,
        Interes, Recargo, Descuento, Total, Fecha, NumRecibo, AnioDeclara,
        FechaPresenta, UsuarioCrea, CodDeclaraIP, NumAvPg, Tasas, RTM)
        VALUES  (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        with self.conexion.cursor() as cur:
            cur.execute(query, data_insert)

    def update_ult_pediodo_fact_contribuyente(self, identidad, ult_periodo):
        query = """UPDATE FC_03 SET UltPeriodoFact = ? WHERE DNI = ?"""
        with self.conexion.cursor() as cur:
            cur.execute(query, ult_periodo, identidad)

    def insertar_solvencia(self, fecha, dni, no_solvencia, anio, usuario, recibo):
        valido = f'{anio}1231'
        query = """INSERT INTO Solvencia (FechaIngreso, Identidad, NoSolvencia, Anio, ValidoHasta, Usuario, NoRecibo) VALUES (?, ?, ?, ?, ?, ?, ?)"""
        with self.conexion.cursor() as cur:
            cur.execute(query, fecha, dni, no_solvencia,
                        anio, valido, usuario, recibo)

    def get_num_solvencia(self,):
        query = """select max(NoSolvencia) as NumSolvencia  from Solvencia """
        with self.conexion.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            if not row:
                return None
            return row[0]+1
