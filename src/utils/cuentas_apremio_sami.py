def clasificar_mora_sami(dato, tipo_impuesto):
    mora = []
    print(dato)
    if isinstance(tipo_impuesto, int):
        tipo_impuesto = str(tipo_impuesto)
    if tipo_impuesto == '0':
        mora = [
                {'cta_ingreso': '11.7.1.01','nombre': 'Impuesto a establecimientos Industriales', 'valor': dato['ic']},
                {'cta_ingreso': '11.7.1.02','nombre': 'Impuesto a establecimientos Comerciales', 'valor': dato['com']},
                {'cta_ingreso': '11.7.1.03','nombre': 'Impuesto a Establecimientos de Servicios', 'valor': dato['ser']},
                {'cta_ingreso': '11.7.2.01', 'nombre': 'Impuesto Sobre Bienes Inmuebles Urbanos', 'valor': dato['bi_urb']},
                {'cta_ingreso': '11.7.2.02', 'nombre': 'Impuesto Sobre Bienes Inmuebles Rurales', 'valor': dato['bi_ru']},
                {'cta_ingreso': '11.7.3.01','nombre': 'Impuesto Personal', 'valor': dato['ip']},
                {'cta_ingreso': '11.7.4.01','nombre': 'Impuesto Extraccion de Recursos','valor': dato['extranccion']},
                {'cta_ingreso': '11.7.5.01','nombre': 'Impuesto Pecuario','valor': dato['pecuario']},
                {'cta_ingreso': '11.7.6.01','nombre': 'Impuesto Selectivo A Telecomunicaciones','valor': dato['telecomunicaciones']},
                {'cta_ingreso': '12.5.99.01', 'nombre': 'Tasas Municipales', 'valor': dato['tasas']},
                {'cta_ingreso': '12.5.99.02', 'nombre': 'Derechos Municipales', 'valor': dato['derecos']},
                {'cta_ingreso': '12.5.99.03', 'nombre': 'Multas Municipales', 'valor': dato['multas']},
                {'cta_ingreso': '15.2.19.02', 'nombre': 'Servicios Municipales', 'valor': dato['servicios']},
                {'cta_ingreso': '15.2.19.98', 'nombre': 'Recuperacion de Servicios Municipales', 'valor': dato['recuperacion_Servicios']},
                {'cta_ingreso': '15.2.19.97', 'nombre': 'Intereses Servicios Municipales', 'valor': dato['intereses_servicios']},
                {'cta_ingreso': '15.2.19.96', 'nombre': 'Recargos Servicios Municipales', 'valor': dato['recargos_servicios']},
                {'cta_ingreso': '11.7.x.98', 'nombre': 'Recuperacion de Impuestos Municipales','valor': dato['recuperacion']},
                {'cta_ingreso': '11.7.x.97', 'nombre': 'Intereses Por Impuestos Municipales','valor': dato['intereses']},
                {'cta_ingreso': '11.7.x.97', 'nombre': 'Recargos Por Impuestos Municipales','valor': dato['recargos']},
            ]
    elif tipo_impuesto == '1':
        mora = [
                {'cta_ingreso': '11.7.2.01', 'nombre': 'Impuesto Sobre Bienes Inmuebles Urbanos', 'valor': dato['bi_urb']},
                {'cta_ingreso': '11.7.2.02', 'nombre': 'Impuesto Sobre Bienes Inmuebles Rurales', 'valor': dato['bi_ru']},
                {'cta_ingreso': '12.5.99.01', 'nombre': 'Tasas Municipales', 'valor': dato['tasas']},
                {'cta_ingreso': '12.5.99.02', 'nombre': 'Derechos Municipales', 'valor': dato['derecos']},
                {'cta_ingreso': '12.5.99.03', 'nombre': 'Multas Municipales', 'valor': dato['multas']},
                {'cta_ingreso': '15.2.19.02', 'nombre': 'Servicios Municipales', 'valor': dato['servicios']},
                {'cta_ingreso': '15.2.19.98', 'nombre': 'Recuperacion de Servicios Municipales', 'valor': dato['recuperacion_Servicios']},
                {'cta_ingreso': '15.2.19.97', 'nombre': 'Intereses Servicios Municipales', 'valor': dato['intereses_servicios']},
                {'cta_ingreso': '15.2.19.96', 'nombre': 'Recargos Servicios Municipales', 'valor': dato['recargos_servicios']},
                {'cta_ingreso': '11.7.x.98', 'nombre': 'Recuperacion de Impuestos Municipales','valor': dato['recuperacion']},
                {'cta_ingreso': '11.7.x.97', 'nombre': 'Intereses Por Impuestos Municipales','valor': dato['intereses']},
                {'cta_ingreso': '11.7.x.97', 'nombre': 'Recargos Por Impuestos Municipales','valor': dato['recargos']},
            ]
    elif tipo_impuesto == '2' or tipo_impuesto == '3':
        mora = [
            {'cta_ingreso': '11.7.1.01','nombre': 'Impuesto a establecimientos Industriales', 'valor': dato['ic']},
            {'cta_ingreso': '11.7.1.02','nombre': 'Impuesto a establecimientos Comerciales', 'valor': dato['com']},
            {'cta_ingreso': '11.7.1.03','nombre': 'Impuesto a Establecimientos de Servicios', 'valor': dato['ser']},
            {'cta_ingreso': '11.7.4.01','nombre': 'Impuesto Extraccion de Recursos','valor': dato['extranccion']},
            {'cta_ingreso': '11.7.5.01','nombre': 'Impuesto Pecuario','valor': dato['pecuario']},
            {'cta_ingreso': '11.7.6.01','nombre': 'Impuesto Selectivo A Telecomunicaciones','valor': dato['telecomunicaciones']},
            {'cta_ingreso': '12.5.99.01', 'nombre': 'Tasas Municipales', 'valor': dato['tasas']},
            {'cta_ingreso': '12.5.99.02', 'nombre': 'Derechos Municipales', 'valor': dato['derecos']},
            {'cta_ingreso': '12.5.99.03', 'nombre': 'Multas Municipales', 'valor': dato['multas']},
            {'cta_ingreso': '15.2.19.02', 'nombre': 'Servicios Municipales', 'valor': dato['servicios']},
            {'cta_ingreso': '15.2.19.98', 'nombre': 'Recuperacion de Servicios Municipales', 'valor': dato['recuperacion_Servicios']},
            {'cta_ingreso': '15.2.19.97', 'nombre': 'Intereses Servicios Municipales', 'valor': dato['intereses_servicios']},
            {'cta_ingreso': '15.2.19.96', 'nombre': 'Recargos Servicios Municipales', 'valor': dato['recargos_servicios']},
            {'cta_ingreso': '11.7.x.98', 'nombre': 'Recuperacion de Impuestos Municipales','valor': dato['recuperacion']},
            {'cta_ingreso': '11.7.x.97', 'nombre': 'Intereses Por Impuestos Municipales','valor': dato['intereses']},
            {'cta_ingreso': '11.7.x.97', 'nombre': 'Recargos Por Impuestos Municipales','valor': dato['recargos']},
        ]
    elif tipo_impuesto == '4':
        mora = [

            {'cta_ingreso': '11.7.3.01','nombre': 'Impuesto Personal', 'valor': dato['ip']},
            {'cta_ingreso': '12.5.99.01', 'nombre': 'Tasas Municipales', 'valor': dato['tasas']},
            {'cta_ingreso': '12.5.99.02', 'nombre': 'Derechos Municipales', 'valor': dato['derecos']},
            {'cta_ingreso': '12.5.99.03', 'nombre': 'Multas Municipales', 'valor': dato['multas']},
            {'cta_ingreso': '15.2.19.02', 'nombre': 'Servicios Municipales', 'valor': dato['servicios']},
            {'cta_ingreso': '15.2.19.98', 'nombre': 'Recuperacion de Servicios Municipales', 'valor': dato['recuperacion_Servicios']},
            {'cta_ingreso': '15.2.19.97', 'nombre': 'Intereses Servicios Municipales', 'valor': dato['intereses_servicios']},
            {'cta_ingreso': '15.2.19.96', 'nombre': 'Recargos Servicios Municipales', 'valor': dato['recargos_servicios']},
            {'cta_ingreso': '11.7.x.98', 'nombre': 'Recuperacion de Impuestos Municipales','valor': dato['recuperacion']},
            {'cta_ingreso': '11.7.x.97', 'nombre': 'Intereses Por Impuestos Municipales','valor': dato['intereses']},
            {'cta_ingreso': '11.7.x.97', 'nombre': 'Recargos Por Impuestos Municipales','valor': dato['recargos']},
        ]

    elif tipo_impuesto == '5':
        mora = [
            {'cta_ingreso': '15.2.19.02', 'nombre': 'Servicios Municipales', 'valor': dato['servicios']},
            {'cta_ingreso': '15.2.19.98', 'nombre': 'Recuperacion de Servicios Municipales', 'valor': dato['recuperacion_Servicios']},
            {'cta_ingreso': '15.2.19.97', 'nombre': 'Intereses Servicios Municipales', 'valor': dato['intereses_servicios']},
            {'cta_ingreso': '15.2.19.96', 'nombre': 'Recargos Servicios Municipales', 'valor': dato['recargos_servicios']},
            {'cta_ingreso': '12.5.99.01', 'nombre': 'Tasas Municipales', 'valor': dato['tasas']},
            {'cta_ingreso': '12.5.99.02', 'nombre': 'Derechos Municipales', 'valor': dato['derecos']},
            {'cta_ingreso': '12.5.99.03', 'nombre': 'Multas Municipales', 'valor': dato['multas']},
        ]
    else:
        mora = [
            {'cta_ingreso': '11.7.1.01','nombre': 'Impuesto a establecimientos Industriales', 'valor': dato['ic']},
            {'cta_ingreso': '11.7.1.02','nombre': 'Impuesto a establecimientos Comerciales', 'valor': dato['com']},
            {'cta_ingreso': '11.7.1.03','nombre': 'Impuesto a Establecimientos de Servicios', 'valor': dato['ser']},
            {'cta_ingreso': '11.7.2.01', 'nombre': 'Impuesto Sobre Bienes Inmuebles Urbanos', 'valor': dato['bi_urb']},
            {'cta_ingreso': '11.7.2.02', 'nombre': 'Impuesto Sobre Bienes Inmuebles Rurales', 'valor': dato['bi_ru']},
            {'cta_ingreso': '11.7.3.01','nombre': 'Impuesto Personal', 'valor': dato['ip']},
            {'cta_ingreso': '11.7.4.01','nombre': 'Impuesto Extraccion de Recursos','valor': dato['extranccion']},
            {'cta_ingreso': '11.7.5.01','nombre': 'Impuesto Pecuario','valor': dato['pecuario']},
            {'cta_ingreso': '11.7.6.01','nombre': 'Impuesto Selectivo A Telecomunicaciones','valor': dato['telecomunicaciones']},
            {'cta_ingreso': '12.5.99.01', 'nombre': 'Tasas Municipales', 'valor': dato['tasas']},
            {'cta_ingreso': '12.5.99.02', 'nombre': 'Derechos Municipales', 'valor': dato['derecos']},
            {'cta_ingreso': '12.5.99.03', 'nombre': 'Multas Municipales', 'valor': dato['multas']},
            {'cta_ingreso': '15.2.19.02', 'nombre': 'Servicios Municipales', 'valor': dato['servicios']},
            {'cta_ingreso': '15.2.19.98', 'nombre': 'Recuperacion de Servicios Municipales', 'valor': dato['recuperacion_Servicios']},
            {'cta_ingreso': '15.2.19.97', 'nombre': 'Intereses Servicios Municipales', 'valor': dato['intereses_servicios']},
            {'cta_ingreso': '15.2.19.96', 'nombre': 'Recargos Servicios Municipales', 'valor': dato['recargos_servicios']},
            {'cta_ingreso': '11.7.x.98', 'nombre': 'Recuperacion de Impuestos Municipales','valor': dato['recuperacion']},
            {'cta_ingreso': '11.7.x.97', 'nombre': 'Intereses Por Impuestos Municipales','valor': dato['intereses']},
            {'cta_ingreso': '11.7.x.97', 'nombre': 'Recargos Por Impuestos Municipales','valor': dato['recargos']},
        ]
    return mora
