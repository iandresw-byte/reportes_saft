from pandas import DataFrame


def sumar_ingresos_depto_diarios_catastro(datos: DataFrame):
    datos["FechaRecibo"] = datos["FechaRecibo"].dt.strftime("%d-%m-%Y")
    # Sumar horizontalmente
    datos["Total_Resultado"] = datos[[
        "VentaDominioPleno",
        "ServiciosDocimentacion",
        "Constancias",
        "MedidasRemedidas",
        "RegistrosPropiedad",
        "Inspeccion",
        "LotesCementerio"]].sum(axis=1)

    datos["Otros"] = datos["TotalReciboPagado"].fillna(
        0) - datos["Total_Resultado"].fillna(0)

    fila_total = {"FechaRecibo": "Total",
                  "VentaDominioPleno": datos["VentaDominioPleno"].sum(),
                  "Constancias": datos["Constancias"].sum(),
                  "ServiciosDocimentacion": datos["ServiciosDocimentacion"].sum(),
                  "MedidasRemedidas": datos["MedidasRemedidas"].sum(),
                  "RegistrosPropiedad": datos["RegistrosPropiedad"].sum(),
                  "LotesCementerio": datos["LotesCementerio"].sum(),
                  "Inspeccion": datos["Inspeccion"].sum(),
                  "TotalReciboPagado": datos["TotalReciboPagado"].sum(),
                  "Total_Resultado": datos["Total_Resultado"].sum(),
                  "Otros": datos["Otros"].sum(),
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["FechaRecibo",
                      "VentaDominioPleno", ""
                      "Constancias",
                      "ServiciosDocimentacion",
                      "MedidasRemedidas",
                      "RegistrosPropiedad",
                      "LotesCementerio",
                      "Inspeccion",
                      "Otros",
                      "TotalReciboPagado",

                      ]]
    nuevo_df.columns = ["Fecha",
                        "Venta de Dominio Pleno",
                        "Constancias",
                        "Servicio de Documentacion",
                        "Servicio de Medidas y Remedidas",
                        "Registros de Propiedad",
                        "Venta de Lotes de Cementerio",
                        "Inspecciones",
                        "Otros",
                        "Total",
                        ]

    return nuevo_df


def sumar_ingresos_depto_diarios_admin_tributaria_os(datos: DataFrame):
    datos["FechaRecibo"] = datos["FechaRecibo"].dt.strftime("%d-%m-%Y")
    datos["Total_Resultado"] = datos[[
        "Constancias",
        "Impuestos",
        "Servicios",
        "Certificaciones",
        "Documentacion",
    ]].sum(axis=1)

    datos["Otros"] = datos["TotalReciboPagado"].fillna(
        0) - datos["Total_Resultado"].fillna(0)

    fila_total = {"FechaRecibo": "",
                  "Constancias": datos["Constancias"].sum(),
                  "Impuestos": datos["Impuestos"].sum(),
                  "Servicios": datos["Servicios"].sum(),
                  "Certificaciones": datos["Certificaciones"].sum(),
                  "Documentacion": datos["Documentacion"].sum(),
                  "TotalReciboPagado": datos["TotalReciboPagado"].sum(),
                  "Total_Resultado": datos["Total_Resultado"].sum(),
                  "Otros": datos["Otros"].sum(),
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total
    nuevo_df = datos[["FechaRecibo",
                      "Constancias",
                      "Impuestos",
                      "Servicios",
                      "Certificaciones",
                      "Documentacion",
                      "Otros",
                      "TotalReciboPagado",
                      ]]
    nuevo_df.columns = ["Fecha",
                        "Constancias",
                        "Impuestos",
                        "Servicios",
                        "Certificaciones",
                        "Documentacion",
                        "Otros",
                        "Total",
                        ]
    return nuevo_df


def sumar_ingresos_depto_diarios_admin_tributaria_bi(datos: DataFrame):
    datos["FechaRecibo"] = datos["FechaRecibo"].dt.strftime("%d-%m-%Y")
    datos["Total_Resultado"] = datos[[
        "ImpuestoBI",
        "RecuperacionBI",
        "Intereses",
        "Recargos",
        "Multas",
        "Bomberos",
        "RecuBomberos",
        "IntereBomberos",
        "RecargosBomberos",
        "descuentos"
    ]].sum(axis=1)
    datos["Total_Impuesto"] = datos[[
        "ImpuestoBI",
        "RecuperacionBI",
    ]].sum(axis=1)
    datos["Total_Intereses"] = datos[[
        "Intereses",
        "IntereBomberos",
    ]].sum(axis=1)
    datos["Total_Recargos"] = datos[[
        "Recargos",
        "RecargosBomberos",
    ]].sum(axis=1)
    datos["Total_bombero"] = datos[[
        "Bomberos",
        "RecuBomberos",
    ]].sum(axis=1)
    datos["Otros"] = datos["TotalReciboPagado"].fillna(
        0) - datos["Total_Resultado"].fillna(0)
    fila_total = {"FechaRecibo": "TOTAL",
                  "ImpuestoBI": datos["ImpuestoBI"].sum(),
                  "RecuperacionBI": datos["RecuperacionBI"].sum(),
                  "Intereses": datos["Intereses"].sum(),
                  "Recargos": datos["Recargos"].sum(),
                  "Multas": datos["Multas"].sum(),
                  "Bomberos": datos["Bomberos"].sum(),
                  "RecuBomberos": datos["RecuBomberos"].sum(),
                  "IntereBomberos": datos["IntereBomberos"].sum(),
                  "RecargosBomberos": datos["RecargosBomberos"].sum(),
                  "descuentos": datos["descuentos"].sum(),
                  "TotalReciboPagado": datos["TotalReciboPagado"].sum(),
                  "Total_Resultado": datos["Total_Resultado"].sum(),
                  "Total_Impuesto": datos["Total_Impuesto"].sum(),
                  "Total_Intereses": datos["Total_Intereses"].sum(),
                  "Total_Recargos": datos["Total_Recargos"].sum(),
                  "Total_bombero": datos["Total_bombero"].sum(),
                  "Otros": datos["Otros"].sum(),
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total
    nuevo_df = datos[["FechaRecibo",
                      "Total_Impuesto",
                      "Total_bombero",
                      "Multas",
                      "Total_Intereses",
                      "Total_Recargos",
                      "Otros",
                      "descuentos",
                      "TotalReciboPagado",
                      ]]
    nuevo_df.columns = ["Fecha",
                        "Impuesto Sobre Bienes Inmuebles",
                        "Servicio de Bomberos",
                        "Multas",
                        "Intereses",
                        "Recargo",
                        "Otros",
                        "Descuentos",
                        "Total",
                        ]
    return nuevo_df


def sumar_ingresos_depto_diarios_admin_tributaria_ics(datos: DataFrame):
    datos["FechaRecibo"] = datos["FechaRecibo"].dt.strftime("%d-%m-%Y")
    # Sumar horizontalmente
    datos["Total_Resultado"] = datos[[
        "Comercio",
        "RecuperacionComercio",
        "PermisoOperacion",
        "Rotulos",
        "Intereses",
        "Recargos",
        "Multas",
        "Bomberos",
        "RecuBomberos",
        "IntereBomberos",
        "RecargosBomberos",
        "descuentos"
    ]].sum(axis=1)

    datos["Total_Impuesto"] = datos[[
        "Comercio",
        "RecuperacionComercio",
    ]].sum(axis=1)

    datos["Total_Intereses"] = datos[[
        "Intereses",
        "IntereBomberos",
    ]].sum(axis=1)

    datos["Total_Recargos"] = datos[[
        "Recargos",
        "RecargosBomberos",
    ]].sum(axis=1)

    datos["Total_bombero"] = datos[[
        "Bomberos",
        "RecuBomberos",
    ]].sum(axis=1)

    datos["Otros"] = datos["TotalReciboPagado"].fillna(
        0) - datos["Total_Resultado"].fillna(0)

    fila_total = {"FechaRecibo": "TOTAL",
                  "Comercio": datos["Comercio"].sum(),
                  "RecuperacionComercio": datos["RecuperacionComercio"].sum(),
                  "PermisoOperacion": datos["PermisoOperacion"].sum(),
                  "Rotulos": datos["Rotulos"].sum(),
                  "Intereses": datos["Intereses"].sum(),
                  "Recargos": datos["Recargos"].sum(),
                  "Multas": datos["Multas"].sum(),
                  "Bomberos": datos["Bomberos"].sum(),
                  "RecuBomberos": datos["RecuBomberos"].sum(),
                  "IntereBomberos": datos["IntereBomberos"].sum(),
                  "RecargosBomberos": datos["RecargosBomberos"].sum(),
                  "descuentos": datos["descuentos"].sum(),
                  "TotalReciboPagado": datos["TotalReciboPagado"].sum(),
                  "Total_Resultado": datos["Total_Resultado"].sum(),
                  "Total_Impuesto": datos["Total_Impuesto"].sum(),
                  "Total_Intereses": datos["Total_Intereses"].sum(),
                  "Total_Recargos": datos["Total_Recargos"].sum(),
                  "Total_bombero": datos["Total_bombero"].sum(),
                  "Otros": datos["Otros"].sum(),
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["FechaRecibo",
                      "Total_Impuesto",
                      "Total_bombero",
                      "PermisoOperacion",
                      "Multas",
                      "Total_Intereses",
                      "Total_Recargos",
                      "Otros",
                      "descuentos",
                      "TotalReciboPagado",
                      ]]
    nuevo_df.columns = ["Fecha",
                        "Impuesto Sobre Industria y Comercio",
                        "Servicio de Bomberos",
                        "Permiso Operacion",
                        "Multas",
                        "Intereses",
                        "Recargo",
                        "Otros",
                        "Descuentos",
                        "Total",
                        ]

    return nuevo_df


def sumar_ingresos_depto_diarios_admin_tributaria_ip(datos: DataFrame):
    datos["FechaRecibo"] = datos["FechaRecibo"].dt.strftime("%d-%m-%Y")
    # Sumar horizontalmente
    datos["Total_Resultado"] = datos[[
        "Impuesto",
        "Recuperacion",
        "Intereses",
        "Recargos",
        "Multas",
        "Solvencia",
        "Descuentos",
    ]].sum(axis=1)

    datos["Otros"] = datos["TotalReciboPagado"].fillna(
        0) - datos["Total_Resultado"].fillna(0)

    fila_total = {"FechaRecibo": "",
                  "Impuesto": datos["Impuesto"].sum(),
                  "Recuperacion": datos["Recuperacion"].sum(),
                  "Intereses": datos["Intereses"].sum(),
                  "Recargos": datos["Recargos"].sum(),
                  "Multas": datos["Multas"].sum(),
                  "Solvencia": datos["Solvencia"].sum(),
                  "Descuentos": datos["Descuentos"].sum(),
                  "TotalReciboPagado": datos["TotalReciboPagado"].sum(),
                  "Total_Resultado": datos["Total_Resultado"].sum(),
                  "Otros": datos["Otros"].sum(),
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["FechaRecibo",
                      "Impuesto",
                      "Recuperacion",
                      "Intereses",
                      "Recargos",
                      "Multas",
                      "Solvencia",
                      "Descuentos",
                      "Otros",
                      "TotalReciboPagado",
                      ]]
    nuevo_df.columns = ["Fecha",
                        "Impuesto",
                        "Recuperacion",
                        "Intereses",
                        "Recargos",
                        "Multas",
                        "Solvencia",
                        "Descuentos",
                        "Otros",
                        "Total",
                        ]

    return nuevo_df


def sumar_ingresos_depto_diarios_uma(datos: DataFrame):
    datos["FechaRecibo"] = datos["FechaRecibo"].dt.strftime("%d-%m-%Y")
    # Sumar horizontalmente
    datos["Total_Resultado"] = datos[[
        "LicenciasExtranccion",
        "BosquesDerivados",
        "TasaAmbiental",
        "MatriculaMotoSierra",
        "PerforacionPozos",
        "Constancias",
        "Inspeccion"]].sum(axis=1)

    datos["Otros"] = datos["TotalReciboPagado"].fillna(
        0) - datos["Total_Resultado"].fillna(0).clip(lower=0)

    datos.columns = [
        "Fecha",
        "Licencias de Extraccion",
        "Bosques y Derivados",
        "Tasa Ambiental",
        "Matricula Moto Sierra",
        "Perforacion de Pozos",
        "Constancias",
        "Inspecciones",
        "Total",
        "Total_Resultado",
        "Otros",
    ]

    fila_total = {"Fecha": "TOTAL",
                  "Licencias de Extraccion": datos["Licencias de Extraccion"].sum(),
                  "Bosques y Derivados": datos["Bosques y Derivados"].sum(),
                  "Tasa Ambiental": datos["Tasa Ambiental"].sum(),
                  "Matricula Moto Sierra": datos["Matricula Moto Sierra"].sum(),
                  "Perforacion de Pozos": datos["Perforacion de Pozos"].sum(),
                  "Constancias": datos["Constancias"].sum(),
                  "Inspecciones": datos["Inspecciones"].sum(),
                  "Total": datos["Total"].sum(),
                  "Total_Resultado": datos["Total_Resultado"].sum(),
                  "Otros": datos["Otros"].sum(),
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["Fecha",
                      "Licencias de Extraccion", ""
                      "Bosques y Derivados",
                      "Tasa Ambiental",
                      "Matricula Moto Sierra",
                      "Perforacion de Pozos",
                      "Constancias",
                      "Inspecciones",
                      "Otros",
                      "Total",
                      ]]

    return nuevo_df


def sumar_ingresos_depto_diarios_justicia(datos: DataFrame):
    datos["FechaRecibo"] = datos["FechaRecibo"].dt.strftime("%d-%m-%Y")
    datos["VistosAutorizacion"] = datos["Autorizaciones"].fillna(
        0) - datos["CartasVenta"].fillna(0).clip(lower=0)
    # Sumar horizontalmente
    datos["Total_Resultado"] = datos[[
        "VistosAutorizacion",
        "CartasVenta",
        "GuiasTransporte",
        "ForjarFierro",
        "MatriculaFierro",
        "MatriculaArmas",
        "Buhunero",
        "InscripcionArrendamiento",
        "Constancias",
    ]].sum(axis=1)

    datos["Otros"] = datos["Totalrecibo"].fillna(
        0) - datos["Total_Resultado"].fillna(0).clip(lower=0)

    fila_total = {"FechaRecibo": "",
                  "Autorizaciones": datos["Autorizaciones"].sum(),
                  "CartasVenta": datos["CartasVenta"].sum(),
                  "GuiasTransporte": datos["GuiasTransporte"].sum(),
                  "ForjarFierro": datos["ForjarFierro"].sum(),
                  "MatriculaFierro": datos["MatriculaFierro"].sum(),
                  "MatriculaArmas": datos["MatriculaArmas"].sum(),
                  "Buhunero": datos["Buhunero"].sum(),
                  "InscripcionArrendamiento": datos["InscripcionArrendamiento"].sum(),
                  "Constancias": datos["Constancias"].sum(),
                  "Totalrecibo": datos["Totalrecibo"].sum(),
                  "VistosAutorizacion": datos["VistosAutorizacion"].sum(),
                  "Total_Resultado": datos["Total_Resultado"].sum(),
                  "Otros": datos["Otros"].sum(),
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["FechaRecibo",
                      "VistosAutorizacion",
                      "CartasVenta",
                      "GuiasTransporte",
                      "ForjarFierro",
                      "MatriculaFierro",
                      "MatriculaArmas",
                      "Buhunero",
                      "InscripcionArrendamiento",
                      "Constancias",
                      "Otros",
                      "Totalrecibo",
                      ]]
    nuevo_df.columns = ["Fecha",
                        "Autorizaciones y Vistos Buenos",
                        "Cartas de Venta",
                        "Guias para Transportar Ganado",
                        "Permiso Para Forjar Marcas de Herrar",
                        "Matrícula de Marcas de Herrar",
                        "Matrícula de Armas",
                        "Licencia Buhuneros",
                        "Inscripciones",
                        "Constancias",
                        "Otros",
                        "Total",
                        ]

    return nuevo_df


def sumar_ingresos_depto_diarios_secretaria(datos: DataFrame):
    datos["FechaRecibo"] = datos["FechaRecibo"].dt.strftime("%d-%m-%Y")
    # Sumar horizontalmente
    datos["Total_Resultado"] = datos[[
        "Matrimonios",
        "Constancias",
        "Certificaciones",
        "VistosBuenos",
    ]].sum(axis=1)

    datos["Otros"] = datos["TotalReciboPagado"].fillna(
        0) - datos["Total_Resultado"].fillna(0)

    fila_total = {"FechaRecibo": "",
                  "Matrimonios": datos["Matrimonios"].sum(),
                  "Constancias": datos["Constancias"].sum(),
                  "Certificaciones": datos["Certificaciones"].sum(),
                  "VistosBuenos": datos["VistosBuenos"].sum(),
                  "TotalReciboPagado": datos["TotalReciboPagado"].sum(),
                  "Total_Resultado": datos["Total_Resultado"].sum(),
                  "Otros": datos["Otros"].sum(),
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["FechaRecibo",
                      "Matrimonios", ""
                      "Constancias",
                      "Certificaciones",
                      "VistosBuenos",
                      "Otros",
                      "TotalReciboPagado",
                      ]]
    nuevo_df.columns = ["Fecha",
                        "Matrimonios", ""
                        "Constancias",
                        "Certificaciones",
                        "Vistos Buenos",
                        "Otros",
                        "Total",
                        ]

    return nuevo_df


def sumar_ingresos_depto_diarios_procamut(datos: DataFrame):
    datos["FechaRecibo"] = datos["FechaRecibo"].dt.strftime("%d-%m-%Y")
    datos["Otros"] = datos["Totalrecibo"].fillna(
        0) - datos["RastroMunicipal"].fillna(0)

    fila_total = {"FechaRecibo": "",
                  "RastroMunicipal": datos["RastroMunicipal"].sum(),
                  "Totalrecibo": datos["Totalrecibo"].sum(),
                  "Otros": datos["Otros"].sum(),
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["FechaRecibo",
                      "RastroMunicipal",
                      "Otros",
                      "Totalrecibo",
                      ]]
    nuevo_df.columns = ["Fecha",
                        "Rastro Municipal", ""
                        "Otros",
                        "Total",
                        ]

    return nuevo_df


def sumar_ingresos_depto_diarios_urbanizacion(datos: DataFrame):
    datos["FechaRecibo"] = datos["FechaRecibo"].dt.strftime("%d-%m-%Y")
    # Sumar horizontalmente
    datos["Total_Resultado"] = datos[[
        "Autorizaciones",
        "LicenciaEjercer",
        "PermisoConstrir",
        "ConstrucccionAntenas",
        "Rotulos",
        "Constancias",
    ]].sum(axis=1)

    datos["Otros"] = datos["Totalrecibo"].fillna(
        0) - datos["Total_Resultado"].fillna(0)

    fila_total = {"FechaRecibo": "",
                  "Autorizaciones": datos["Autorizaciones"].sum(),
                  "LicenciaEjercer": datos["LicenciaEjercer"].sum(),
                  "PermisoConstrir": datos["PermisoConstrir"].sum(),
                  "ConstrucccionAntenas": datos["ConstrucccionAntenas"].sum(),
                  "Rotulos": datos["Rotulos"].sum(),
                  "Constancias": datos["Constancias"].sum(),
                  "Totalrecibo": datos["Totalrecibo"].sum(),
                  "Total_Resultado": datos["Total_Resultado"].sum(),
                  "Otros": datos["Otros"].sum(),
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["FechaRecibo",
                      "Autorizaciones",
                      "LicenciaEjercer",
                      "PermisoConstrir",
                      "ConstrucccionAntenas",
                      "Rotulos",
                      "Constancias",
                      "Otros",
                      "Totalrecibo",
                      ]]
    nuevo_df.columns = ["Fecha",
                        "Autorizaciones", ""
                        "Licencias para Ejercer",
                        "Permisos de Construcción",
                        "Permisos de Construcción de Antenas",
                        "Instlación de Rótulos",
                        "Constancias",
                        "Otros",
                        "Total",
                        ]

    return nuevo_df
