import pandas as pd
from datetime import datetime
from src.models.declaracion_ip import DeclaraNat
from src.repositories.finalizar_pago_ip import FinalizarPagosIPRepository, DeclaraImpInd
from src.ui.PagosIP.utils_pagos_ip import snack_inicio_reporte


class FinalizarPagosIPService:
    def __init__(self, appContext, sistem):
        self.conexion = appContext.conexion_saft
        self.user = appContext.usuario_actual
        self.repositorio = FinalizarPagosIPRepository(self.conexion)
        self.sys = sistem

    def relacionar_pago_otras_tasas(self, vista, caja, num_recibo: int, ruta: str, ):
        data_existe = self.repositorio.existe_pago(num_recibo)
        if data_existe:
            raise Exception('Este Recibo ya fue utilizado')
        data = self.repositorio.get_recibo(num_recibo)
        num_decrara = self.repositorio.get_ult_cod_decracion()
        cod_declara = f"IP{num_decrara}"
        if data is None:
            raise Exception('No se encontro informaciondel recibo')
        caja.value = ""
        vista.escribir_progreso("Iniciando proceso...")
        vista.escribir_progreso(f"Archivo: {ruta}")
        vista.escribir_progreso(f"Recibo: {num_recibo}")

        df = pd.read_excel(
            ruta,
            header=8,
            usecols="A:M",
            dtype={"Identidad": str}
        )
        data_declaracion_nat = []

        num_fila_totales = len(df)-1
        decracion = DeclaraImpInd(
            Identidad="",
            FechaPresenta=datetime.today(),
            PeriodoDeclara=0,
            Impuesto=df.loc[num_fila_totales, "Impuesto"],  # type: ignore
            CodDeclaraIP=cod_declara,
            EstadoDeclaraIP=0,
            IngSueldos=df.loc[num_fila_totales, "Ingreso"],  # type: ignore
            Descuento=df.loc[num_fila_totales, "Descuento"],  # type: ignore
            MultaDeclaraTardeIP=df.loc[num_fila_totales, "Multa"],
            RecMoraIP=df.loc[num_fila_totales, "Interes"],  # type: ignore
            RecSobreSaldoIP=df.loc[num_fila_totales,
                                   "Recargo"])  # type: ignore
        total = len(data)

        contador = 0
        num_factura = 0

        for rec in data:
            decracion.Identidad = rec[2]
            decracion.FechaPresenta = rec[1]
            decracion.FechaPagoIP = rec[1]
            num_factura = rec[4]
            decracion.PeriodoDeclara = rec[1].year
            break

        self.repositorio.crear_declaracion(decracion)
        vista.escribir_progreso("Realizando declaracion...")
        total = len(df)
        contador = 0
        for row in df.itertuples():
            if total-2 <= contador:
                continue

            data_declaracion_nat.append(DeclaraNat(
                Empresa=row[1],
                Identidad=str((row[2])),
                Nombre=str((row[3])),
                Ingreso=row[4],
                Impuesto=row[5],
                Multa=row[6],
                Interes=row[7],
                Recargo=row[8],
                Descuento=row[9],
                Total=row[11],
                Fecha=row[13],
                NumRecibo=num_recibo,
                AnioDeclara=decracion.PeriodoDeclara,
                FechaPresenta=decracion.FechaPresenta,
                UsuarioCrea=self.user.username,
                CodDeclaraIP=cod_declara,
                NumAvPg=num_factura,
                Tasas=row[9],
                RTM=decracion.Identidad,
            ))
            contador += 1

        for row in data_declaracion_nat:
            self.repositorio.insertar_declaracion_natural_empresa(row)
            vista.escribir_progreso(f"Procesando: {row.Identidad}")
            self.repositorio.update_ult_pediodo_fact_contribuyente(
                row.Identidad, row.AnioDeclara)
            vista.escribir_progreso(
                f"Aplicando ultimo perido: {row.AnioDeclara} a  {row.Identidad} {row.Nombre}")
            num_solvencia = self.repositorio.get_num_solvencia()
            self.repositorio.insertar_solvencia(
                row.Fecha, row.Identidad, num_solvencia, row.AnioDeclara, '', row.NumRecibo, )
            vista.escribir_progreso(
                f"Solvencia No.{num_solvencia} Generada a  {row.Identidad}  {row.Nombre}")
        vista.escribir_progreso(
            f"¡Finalizo!")
        return True
