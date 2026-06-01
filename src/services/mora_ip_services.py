from src.repositories.facturas_repository import FacturasRepository
from src.repositories.cuenta_ingreso_repository import CuentaIngresoRepository
from src.services.parametro_service import ParametroService


class MoraIPService:
    def __init__(self, conexion, sistem):
        self.repo_factura = FacturasRepository(conexion)
        self.repo_cta_ingreso = CuentaIngresoRepository(conexion)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem

    def obtener_mora_ip(self):
        cta_ip = self.sys['CtaIngresoIP']
        datos = []
        data_cta_ip = self.repo_cta_ingreso.obtener_cuentas(cta_ip)

        mora_ip = self.repo_factura.obtener_mora_ip(
            data_cta_ip['CtaIngreso'])  # type: ignore
        if mora_ip:
            valor = mora_ip['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': data_cta_ip['CtaIngreso'],  # type: ignore
            'Tipo': 'Saldo Año Actual Impuesto Personal',
            'Valor': valor
        })


# INTERESES
        interes_ip = self.repo_factura.obtener_int_rec_ip(
            data_cta_ip['CtaInteres'])  # type: ignore
        if interes_ip:
            valor = interes_ip['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': data_cta_ip['CtaInteres'],  # type: ignore
            'Tipo': 'Intereses Sobre Impuesto Personal',
            'Valor': valor
        })

 # RECARGOS
        recargos_ip = self.repo_factura.obtener_int_rec_ip(
            data_cta_ip['CtaRecargos']  # type: ignore
        )
        if recargos_ip:
            valor = recargos_ip['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': data_cta_ip['CtaRecargos'],  # type: ignore
            'Tipo': 'Recargos Sobre Impuesto Personal',
            'Valor': valor
        })


# RECUPERACION
        recuperacion_ip = self.repo_factura.obtener_mora_ip(
            data_cta_ip['CtaRecuperacion']  # type: ignore
        )
        if recuperacion_ip:
            valor = recuperacion_ip['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': data_cta_ip['CtaRecuperacion'],  # type: ignore
            'Tipo': 'Recuperación de Saldos Sobre Impuesto Personal',
            'Valor': valor
        })

        if not datos:
            raise ValueError("No se encontraron datos de mora BI.")
        return datos
