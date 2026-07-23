def get_tipo_impuesto(self, tipo_impuesto=None):
        if tipo_impuesto == '%':
            return "Impuestos, Tasas y Servicios Municipales"
        elif tipo_impuesto == '0':
            return "Otras Tasas y Servicios Municipales"
        elif tipo_impuesto == '1':
            return "Impuestos Sobre Bienes Inmuebles"
        elif tipo_impuesto == '2':
            return "Impuesto de Sobre Industria, Comercio y Servicio"
        elif tipo_impuesto == '3':
            return "Tasas de Permiso de Operacion"
        elif tipo_impuesto == '4':
            return "Impuesto Personal"
        elif tipo_impuesto == '5':
            return "Servicios Publicos Municipales"
        elif tipo_impuesto == '7':
            return "Planes de Pago"
        else:
            return "Otros No Clasificados"