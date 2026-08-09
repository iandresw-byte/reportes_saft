from src.ui.components.ui_botones import create_boton


def botones_mora(vista):
    return [
        create_boton("Mora Bienes Inmuebles", vista.on_mora_bi),
        create_boton("Mora Impuesto Personal", vista.on_mora_ip),
        create_boton("Mora Industria Comercio y Servicio", vista.on_mora_ics),
        create_boton("Mora Servicios Públicos", vista.on_mora_sp),
        create_boton("Mora vs Ingresos Aldea General",
                     vista.abrir_modal_mora_vs_ingresos),
        create_boton("Mora vs Ingresos BI (Aldea - Año)",
                     vista.abrir_modal_mora_aldea_anio),
        
        
        
        create_boton("Estratificacion INE",
                     vista.abrir_modal_estratificacion_ine),
        create_boton("Estratificacion Declaraciones SAR",
                     vista.abrir_modal_estratificacion_sar),
        create_boton("Abonados en Mora Por Tipo de Servicio",vista.abrir_modal_mora_abona_x_tipo),
        create_boton("Establecimientos en Mora Por Actividad Economica",vista.abrir_modal_mora_comercio_x_tipo),
    ]


def botones_ingresos(vista):
    return [
        create_boton("Ingresos Generales por Departamento",
                     vista.abrir_modal_ingresos_depto),
        create_boton("Ingresos Detallados Por Contribuyente (Departamentos)",
                     vista.abrir_modal_ingresos_detallados_depto),
        create_boton("Ingresos Diarios (Departamentos)",
                     vista.abrir_modal_ingresos_diarios_depto),
        create_boton("Ingresos Mensuales (Departamentos)",
                     vista.abrir_modal_ingresos_mensual_depto),
        create_boton("Ingresos Bomberos",
                     vista.abrir_modal_ingresos_bomberos),
        create_boton("Analisis de Ingresos Cuentas Gobernacion",
                             vista.abril_modal_analisi_ingresos),
        create_boton("Reporte Permiso Operacion",
                             vista.abril_modal_rpt_permisos_operacion),
    ]


def botones_otros(vista):
    return [
        create_boton("Transición y Traspaso",
                     vista.abril_modal_trancicion),
        create_boton("Detalle IP", vista.rpt_trancicion_det_ip),
        create_boton("Detalle BI", vista.rpt_trancicion_det_bi),
        create_boton("Detalle ICS", vista.rpt_trancicion_det_ics),
        create_boton("Detalle AMB", vista.rpt_trancicion_det_amp),
        create_boton("Detalle IST", vista.rpt_trancicion_det_ist),
        create_boton("Detalle SP", vista.rpt_trancicion_det_sp),
    ]


def botones_herramientas(vista):
    return [
        create_boton("Tarjera Unica",
                     vista.abril_modal_tarjeta_unica),
        create_boton("Anula Plan de Pago", vista.abril_modal_anula_pp),
  ]
