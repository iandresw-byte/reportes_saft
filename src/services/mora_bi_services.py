from src.repositories.facturas_repository import FacturasRepository
from src.repositories.cuenta_ingreso_repository import CuentaIngresoRepository
from src.services.parametro_service import ParametroService


class MoraBIService:
    def __init__(self, conexion, sistem):
        self.repo_factura = FacturasRepository(conexion)
        self.repo_cta_ingreso = CuentaIngresoRepository(conexion)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem

    def obtener_mora_bi_sami(self):
        cta_bi_urbano = self.sys['CtaIngresoBiUrb']
        cta_bi_rural = self.sys['CtaIngresoBiRural']

        datos = []

        data_cta_urbano = self.repo_cta_ingreso.obtener_cuentas(cta_bi_urbano)
        data_cta_rural = self.repo_cta_ingreso.obtener_cuentas(cta_bi_rural)

        mora_urbano = self.repo_factura.obtener_mora_bi(
            data_cta_urbano['CtaIngreso'])
        if mora_urbano:
            valor = mora_urbano['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': data_cta_urbano['CtaIngreso'].replace(" ", ""),
            'Tipo': 'Mora Año Actual Impuesto Sobre Bienes Inmuebles Urbanos',
            'Valor': valor
        })

        mora_rural = self.repo_factura.obtener_mora_bi(
            data_cta_rural['CtaIngreso'])
        if mora_rural:
            valor = mora_rural['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': data_cta_rural['CtaIngreso'].replace(" ", ""),
            'Tipo': 'Mora Año Actual Impuesto Sobre Bienes Inmuebles Rural',
            'Valor': valor
        })

# INTERESES
        interes_bi_urbano = self.repo_factura.obtener_mora_bi(
            data_cta_urbano['CtaInteres'])
        if interes_bi_urbano:
            valor = interes_bi_urbano['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': data_cta_urbano['CtaInteres'].replace(" ", ""),
            'Tipo': 'Intereses Sobre Bienes Inmuebles Urbanos',
            'Valor': valor
        })

        interes_bi_rural = self.repo_factura.obtener_mora_bi(
            data_cta_rural['CtaInteres'])
        if interes_bi_rural:
            valor = interes_bi_rural['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': data_cta_rural['CtaInteres'].replace(" ", ""),
            'Tipo': 'Intereses Sobre Bienes Inmuebles Rural',
            'Valor': valor
        })

 # RECARGOS
        recargos_bi_urbanos = self.repo_factura.obtener_mora_bi(
            data_cta_urbano['CtaRecargos']
        )
        if recargos_bi_urbanos:
            valor = recargos_bi_urbanos['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': data_cta_urbano['CtaRecargos'].replace(" ", ""),
            'Tipo': 'Recargos Sobre Bienes Inmuebles Urbanos',
            'Valor': valor
        })

        recargos_bi_rurales = self.repo_factura.obtener_mora_bi(
            data_cta_rural['CtaRecargos']
        )
        if recargos_bi_rurales:
            valor = recargos_bi_rurales['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': data_cta_rural['CtaRecargos'].replace(" ", ""),
            'Tipo': 'Recargos Sobre Bienes Inmuebles Rurales',
            'Valor': valor
        })


# RECUPERACION
        recuperacion_bi_urb = self.repo_factura.obtener_mora_bi(
            data_cta_urbano['CtaRecuperacion']
        )
        if recuperacion_bi_urb:
            valor = recuperacion_bi_urb['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': data_cta_urbano['CtaRecuperacion'].replace(" ", ""),
            'Tipo': 'Recuperación de Saldos Sobre Bienes Inmuebles Urbanos',
            'Valor': valor
        })

        recuperacion_bi_ru = self.repo_factura.obtener_mora_bi(
            data_cta_rural['CtaRecuperacion']
        )
        if recuperacion_bi_ru:
            valor = recuperacion_bi_ru['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': data_cta_rural['CtaRecuperacion'].replace(" ", ""),
            'Tipo': 'Recuperación de Saldos Sobre Bienes Inmuebles Rural',
            'Valor': valor
        })

        if not datos:
            raise ValueError("No se encontraron datos de mora BI.")
        return datos

    def obtener_mora_bi_gob(self):
        cta_bi_urbano = self.sys['CtaIngresoBiUrb']
        cta_bi_rural = self.sys['CtaIngresoBiRural']
        cta_recargo_bi_impuesto = self.sys['CtaIngresoRecargoImp']
        cta_interes_bi_impuesto = self.sys['CtaIngresoIntImp']

        datos = []

        data_cta_urbano = self.repo_cta_ingreso.obtener_cuentas(cta_bi_urbano)
        data_cta_rural = self.repo_cta_ingreso.obtener_cuentas(cta_bi_rural)

        mora_urbano = self.repo_factura.obtener_mora_bi(
            data_cta_urbano['CtaIngreso'])
        if mora_urbano:
            valor = mora_urbano['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': data_cta_urbano['CtaIngreso'].replace(" ", ""),
            'Tipo': 'Mora Año Actual Impuesto Sobre Bienes Inmuebles Urbanos',
            'Valor': valor
        })

        mora_rural = self.repo_factura.obtener_mora_bi(
            data_cta_rural['CtaIngreso'])
        if mora_rural:
            valor = mora_rural['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': data_cta_rural['CtaIngreso'].replace(" ", ""),
            'Tipo': 'Mora Año Actual Impuesto Sobre Bienes Inmuebles Rural',
            'Valor': valor
        })

# INTERESES
        interes_bi_urbano = self.repo_factura.obtener_mora_bi(
            cta_interes_bi_impuesto)
        if interes_bi_urbano:
            valor = interes_bi_urbano['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': cta_interes_bi_impuesto.replace(" ", ""),
            'Tipo': 'Intereses Sobre Bienes Inmuebles',
            'Valor': valor
        })

 # RECARGOS
        recargos_bi_urbanos = self.repo_factura.obtener_mora_bi(
            cta_recargo_bi_impuesto
        )
        if recargos_bi_urbanos:
            valor = recargos_bi_urbanos['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': cta_recargo_bi_impuesto.replace(" ", ""),
            'Tipo': 'Recargos Sobre Bienes Inmuebles',
            'Valor': valor
        })

        # RECUPERACION
        recuperacion_bi_urb = self.repo_factura.obtener_mora_bi(
            data_cta_urbano['CtaRecuperacion']
        )
        if recuperacion_bi_urb:
            valor = recuperacion_bi_urb['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': data_cta_urbano['CtaRecuperacion'].replace(" ", ""),
            'Tipo': 'Recuperación de Saldos Sobre Bienes Inmuebles Urbanos',
            'Valor': valor
        })

        recuperacion_bi_ru = self.repo_factura.obtener_mora_bi(
            data_cta_rural['CtaRecuperacion']
        )
        if recuperacion_bi_ru:
            valor = recuperacion_bi_ru['valor']
        else:
            valor = 0
        datos.append({
            'Cuenta': data_cta_rural['CtaRecuperacion'].replace(" ", ""),
            'Tipo': 'Recuperación de Saldos Sobre Bienes Inmuebles Rural',
            'Valor': valor
        })

        if not datos:
            raise ValueError("No se encontraron datos de mora BI.")
        return datos
