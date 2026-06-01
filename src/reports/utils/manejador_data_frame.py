from pandas import DataFrame


def sumar_ingresos_departo_catastro(datos: DataFrame):

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
    datos["Nombre_Completo"] = (
        datos["Pnombre"].fillna('') + ' ' +
        datos["SNombre"].fillna('') + ' ' +
        datos["PApellido"].fillna('') + ' ' +
        datos["SApellido"].fillna('')
    ).str.replace(r'\s+', ' ', regex=True).str.strip()

    fila_total = {"FechaRecibo": "",
                  "NumRecibo": "",
                  "DNI": "",
                  "Pnombre": "",
                  "SNombre": "",
                  "PApellido": "",
                  "SApellido": "",
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
                  "Nombre_Completo": "Total",
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["NumRecibo", "DNI", "Nombre_Completo",
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
    nuevo_df.columns = ["No. Recibo", "DNI", "Nombre Completo",
                        "Venta de Dominio Pleno",
                        "Constancias",
                        "Servicio de Documentacion",
                        "Servicio de Medidas y Remedidas",
                        "Registros de Propiedad",
                        "Venta de Lotes de Cementerio",
                        "Inspecciones",
                        "Otros",
                        "Total Recibo",
                        ]

    return nuevo_df


def sumar_ingresos_departo_admin_tributaria_os(datos: DataFrame):
    datos["Total_Resultado"] = datos[[
        "Constancias",
        "Impuestos",
        "Servicios",
        "Certificaciones",
        "Documentacion",
    ]].sum(axis=1)

    datos["Otros"] = datos["TotalReciboPagado"].fillna(
        0) - datos["Total_Resultado"].fillna(0)
    datos["Nombre_Completo"] = (
        datos["Pnombre"].fillna('') + ' ' +
        datos["SNombre"].fillna('') + ' ' +
        datos["PApellido"].fillna('') + ' ' +
        datos["SApellido"].fillna('')
    ).str.replace(r'\s+', ' ', regex=True).str.strip()
    fila_total = {"FechaRecibo": "",
                  "NumRecibo": "",
                  "DNI": "",
                  "Pnombre": "",
                  "SNombre": "",
                  "PApellido": "",
                  "SApellido": "",
                  "ClaveCatastro": "",
                  "Constancias": datos["Constancias"].sum(),
                  "Impuestos": datos["Impuestos"].sum(),
                  "Servicios": datos["Servicios"].sum(),
                  "Certificaciones": datos["Certificaciones"].sum(),
                  "Documentacion": datos["Documentacion"].sum(),
                  "TotalReciboPagado": datos["TotalReciboPagado"].sum(),
                  "Total_Resultado": datos["Total_Resultado"].sum(),
                  "Otros": datos["Otros"].sum(),
                  "Nombre_Completo": "Total",
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total
    nuevo_df = datos[["NumRecibo",
                      "DNI",
                      "Nombre_Completo",
                      "Constancias",
                      "Impuestos",
                      "Servicios",
                      "Certificaciones",
                      "Documentacion",
                      "Otros",
                      "TotalReciboPagado",
                      ]]
    nuevo_df.columns = ["No. Recibo",
                        "DNI",
                        "Nombre Completo",
                        "Constancias",
                        "Impuestos",
                        "Servicios",
                        "Certificaciones",
                        "Documentacion",
                        "Otros",
                        "Total Recibo",
                        ]
    return nuevo_df


def sumar_ingresos_departo_admin_tributaria_bi(datos: DataFrame):
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
    datos["Nombre_Completo"] = (
        datos["Pnombre"].fillna('') + ' ' +
        datos["SNombre"].fillna('') + ' ' +
        datos["PApellido"].fillna('') + ' ' +
        datos["SApellido"].fillna('')
    ).str.replace(r'\s+', ' ', regex=True).str.strip()
    fila_total = {"FechaRecibo": "",
                  "NumRecibo": "",
                  "DNI": "",
                  "Pnombre": "",
                  "SNombre": "",
                  "PApellido": "",
                  "SApellido": "",
                  "ClaveCatastro": "",
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
                  "Nombre_Completo": "Total",
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total
    nuevo_df = datos[["NumRecibo",
                      "DNI",
                      "Nombre_Completo",
                      "ClaveCatastro",
                      "Total_Impuesto",
                      "Total_bombero",
                      "Multas",
                      "Total_Intereses",
                      "Total_Recargos",
                      "Otros",
                      "descuentos",
                      "TotalReciboPagado",
                      ]]
    nuevo_df.columns = ["No. Recibo",
                        "DNI",
                        "Nombre Completo",
                        "Clave Catastro",
                        "Impuesto Sobre Bienes Inmuebles",
                        "Servicio de Bomberos",
                        "Multas",
                        "Intereses",
                        "Recargo",
                        "Otros",
                        "Descuentos",
                        "Total Recibo",
                        ]
    return nuevo_df


def sumar_ingresos_departo_admin_tributaria_ics(datos: DataFrame):

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
    datos["Nombre_Completo"] = (datos["Pnombre"].fillna(
        '')).str.replace(r'\s+', ' ', regex=True).str.strip()

    fila_total = {"FechaRecibo": "",
                  "NumRecibo": "",
                  "DNI": "",
                  "Pnombre": "",
                  "NombreCtaIngreso": "",
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
                  "Nombre_Completo": "Total",
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["NumRecibo",
                      "DNI",
                      "Nombre_Completo",
                      "NombreCtaIngreso",
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
    nuevo_df.columns = ["No. Recibo",
                        "DNI",
                        "Nombre Completo",
                        "Actividad Economica",
                        "Impuesto Sobre Industria y Comercio",
                        "Servicio de Bomberos",
                        "Permiso Operacion",
                        "Multas",
                        "Intereses",
                        "Recargo",
                        "Otros",
                        "Descuentos",
                        "Total Recibo",
                        ]

    return nuevo_df


def sumar_ingresos_departo_admin_tributaria_ip(datos: DataFrame):

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
    datos["Nombre_Completo"] = (
        datos["Pnombre"].fillna('') + ' ' +
        datos["SNombre"].fillna('') + ' ' +
        datos["PApellido"].fillna('') + ' ' +
        datos["SApellido"].fillna('')
    ).str.replace(r'\s+', ' ', regex=True).str.strip()
    fila_total = {"FechaRecibo": "",
                  "NumRecibo": "",
                  "DNI": "",
                  "Pnombre": "",
                  "SNombre": "",
                  "PApellido": "",
                  "SApellido": "",
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
                  "Nombre_Completo": "Total",
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["NumRecibo",
                      "DNI",
                      "Nombre_Completo",
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
    nuevo_df.columns = ["No. Recibo",
                        "DNI",
                        "Nombre Completo",
                        "Impuesto",
                        "Recuperacion",
                        "Intereses",
                        "Recargos",
                        "Multas",
                        "Solvencia",
                        "Descuentos",
                        "Otros",
                        "Total Recibo",
                        ]

    return nuevo_df


def sumar_ingresos_departo_uma(datos: DataFrame):

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
    datos["Nombre_Completo"] = (
        datos["Pnombre"].fillna('') + ' ' +
        datos["SNombre"].fillna('') + ' ' +
        datos["PApellido"].fillna('') + ' ' +
        datos["SApellido"].fillna('')
    ).str.replace(r'\s+', ' ', regex=True).str.strip()

    datos.columns = [
        "Fecha Recibo",
        "No. Recibo",
        "DNI",
        "Pnombre",
        "SNombre",
        "PApellido",
        "SApellido",
        "Licencias de Extraccion",
        "Bosques y Derivados",
        "Tasa Ambiental",
        "Matricula Moto Sierra",
        "Perforacion de Pozos",
        "Constancias",
        "Inspecciones",
        "Total Recibo",
        "Total_Resultado",
        "Otros",
        "Nombre Completo"
    ]

    fila_total = {"Fecha Recibo": "",
                  "No. Recibo": "",
                  "DNI": "",
                  "Pnombre": "",
                  "SNombre": "",
                  "PApellido": "",
                  "SApellido": "",
                  "Licencias de Extraccion": datos["Licencias de Extraccion"].sum(),
                  "Bosques y Derivados": datos["Bosques y Derivados"].sum(),
                  "Tasa Ambiental": datos["Tasa Ambiental"].sum(),
                  "Matricula Moto Sierra": datos["Matricula Moto Sierra"].sum(),
                  "Perforacion de Pozos": datos["Perforacion de Pozos"].sum(),
                  "Constancias": datos["Constancias"].sum(),
                  "Inspecciones": datos["Inspecciones"].sum(),
                  "Total Recibo": datos["Total Recibo"].sum(),
                  "Total_Resultado": datos["Total_Resultado"].sum(),
                  "Otros": datos["Otros"].sum(),
                  "Nombre Completo": "Total",
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["No. Recibo", "DNI", "Nombre Completo",
                      "Licencias de Extraccion", ""
                      "Bosques y Derivados",
                      "Tasa Ambiental",
                      "Matricula Moto Sierra",
                      "Perforacion de Pozos",
                      "Constancias",
                      "Inspecciones",
                      "Otros",
                      "Total Recibo",

                      ]]

    return nuevo_df


def sumar_ingresos_departo_justicia(datos: DataFrame):

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

    datos["Nombre_Completo"] = (
        datos["Pnombre"].fillna('') + ' ' +
        datos["SNombre"].fillna('') + ' ' +
        datos["PApellido"].fillna('') + ' ' +
        datos["SApellido"].fillna('')
    ).str.replace(r'\s+', ' ', regex=True).str.strip()

    fila_total = {"FechaRecibo": "",
                  "NumRecibo": "",
                  "DNI": "",
                  "Pnombre": "",
                  "SNombre": "",
                  "PApellido": "",
                  "SApellido": "",
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
                  "Nombre_Completo": "Total",
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["NumRecibo", "DNI", "Nombre_Completo",
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
    nuevo_df.columns = ["No. Recibo", "DNI", "Nombre Completo",
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
                        "Total Recibo",
                        ]

    return nuevo_df


def sumar_ingresos_departo_secretaria(datos: DataFrame):

    # Sumar horizontalmente
    datos["Total_Resultado"] = datos[[
        "Matrimonios",
        "Constancias",
        "Certificaciones",
        "VistosBuenos",
    ]].sum(axis=1)

    datos["Otros"] = datos["TotalReciboPagado"].fillna(
        0) - datos["Total_Resultado"].fillna(0)
    datos["Nombre_Completo"] = (
        datos["Pnombre"].fillna('') + ' ' +
        datos["SNombre"].fillna('') + ' ' +
        datos["PApellido"].fillna('') + ' ' +
        datos["SApellido"].fillna('')
    ).str.replace(r'\s+', ' ', regex=True).str.strip()

    fila_total = {"FechaRecibo": "",
                  "NumRecibo": "",
                  "DNI": "",
                  "Pnombre": "",
                  "SNombre": "",
                  "PApellido": "",
                  "SApellido": "",
                  "Matrimonios": datos["Matrimonios"].sum(),
                  "Constancias": datos["Constancias"].sum(),
                  "Certificaciones": datos["Certificaciones"].sum(),
                  "VistosBuenos": datos["VistosBuenos"].sum(),
                  "TotalReciboPagado": datos["TotalReciboPagado"].sum(),
                  "Total_Resultado": datos["Total_Resultado"].sum(),
                  "Otros": datos["Otros"].sum(),
                  "Nombre_Completo": "Total",
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["NumRecibo", "DNI", "Nombre_Completo",
                      "Matrimonios", ""
                      "Constancias",
                      "Certificaciones",
                      "VistosBuenos",
                      "Otros",
                      "TotalReciboPagado",
                      ]]
    nuevo_df.columns = ["No. Recibo", "DNI", "Nombre Completo",
                        "Matrimonios", ""
                        "Constancias",
                        "Certificaciones",
                        "Vistos Buenos",
                        "Otros",
                        "Total Recibo",
                        ]

    return nuevo_df


def sumar_ingresos_depto_procamut(datos: DataFrame):

    datos["Otros"] = datos["Totalrecibo"].fillna(
        0) - datos["RastroMunicipal"].fillna(0)
    datos["Nombre_Completo"] = (
        datos["Pnombre"].fillna('') + ' ' +
        datos["SNombre"].fillna('') + ' ' +
        datos["PApellido"].fillna('') + ' ' +
        datos["SApellido"].fillna('')
    ).str.replace(r'\s+', ' ', regex=True).str.strip()

    fila_total = {"FechaRecibo": "",
                  "NumRecibo": "",
                  "DNI": "",
                  "Pnombre": "",
                  "SNombre": "",
                  "PApellido": "",
                  "SApellido": "",
                  "RastroMunicipal": datos["RastroMunicipal"].sum(),
                  "Totalrecibo": datos["Totalrecibo"].sum(),
                  "Otros": datos["Otros"].sum(),
                  "Nombre_Completo": "Total",
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["NumRecibo", "DNI", "Nombre_Completo",
                      "RastroMunicipal",
                      "Otros",
                      "Totalrecibo",
                      ]]
    nuevo_df.columns = ["No. Recibo", "DNI", "Nombre Completo",
                        "Rastro Municipal", ""
                        "Otros",
                        "Total Recibo",
                        ]

    return nuevo_df


def sumar_ingresos_depto_urbanizacion(datos: DataFrame):

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
    datos["Nombre_Completo"] = (
        datos["Pnombre"].fillna('') + ' ' +
        datos["SNombre"].fillna('') + ' ' +
        datos["PApellido"].fillna('') + ' ' +
        datos["SApellido"].fillna('')
    ).str.replace(r'\s+', ' ', regex=True).str.strip()

    fila_total = {"FechaRecibo": "",
                  "NumRecibo": "",
                  "DNI": "",
                  "Pnombre": "",
                  "SNombre": "",
                  "PApellido": "",
                  "SApellido": "",
                  "Autorizaciones": datos["Autorizaciones"].sum(),
                  "LicenciaEjercer": datos["LicenciaEjercer"].sum(),
                  "PermisoConstrir": datos["PermisoConstrir"].sum(),
                  "ConstrucccionAntenas": datos["ConstrucccionAntenas"].sum(),
                  "Rotulos": datos["Rotulos"].sum(),
                  "Constancias": datos["Constancias"].sum(),
                  "Totalrecibo": datos["Totalrecibo"].sum(),
                  "Total_Resultado": datos["Total_Resultado"].sum(),
                  "Otros": datos["Otros"].sum(),
                  "Nombre_Completo": "Total",
                  }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["NumRecibo", "DNI", "Nombre_Completo",
                      "Autorizaciones",
                      "LicenciaEjercer",
                      "PermisoConstrir",
                      "ConstrucccionAntenas",
                      "Rotulos",
                      "Constancias",
                      "Otros",
                      "Totalrecibo",
                      ]]
    nuevo_df.columns = ["No. Recibo", "DNI", "Nombre Completo",
                        "Autorizaciones", ""
                        "Licencias para Ejercer",
                        "Permisos de Construcción",
                        "Permisos de Construcción de Antenas",
                        "Instlación de Rótulos",
                        "Constancias",
                        "Otros",
                        "Total Recibo",
                        ]

    return nuevo_df


def sumar_ingresos_bomberos_sami(datos: DataFrame):

    # Sumar horizontalmente
    datos["Total_Resultado"] = datos[[
        "saldo",
        "recargos",
        "intereses",
        "recuperacion"
    ]].sum(axis=1)

    datos["Nombre_Completo"] = (
        datos["Pnombre"].fillna('') + ' ' +
        datos["SNombre"].fillna('') + ' ' +
        datos["PApellido"].fillna('') + ' ' +
        datos["SApellido"].fillna('')
    ).str.replace(r'\s+', ' ', regex=True).str.strip()

    fila_total = {
        "DNI": "",
        "Pnombre": "",
        "SNombre": "",
        "PApellido": "",
        "SApellido": "",
        "saldo": datos["saldo"].sum(),
        "recargos": datos["recargos"].sum(),
        "intereses": datos["intereses"].sum(),
        "recuperacion": datos["recuperacion"].sum(),
        "NumRecibo": '',
        "Total_Resultado": datos["Total_Resultado"].sum(),
        "Nombre_Completo": "Total",
    }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["NumRecibo",
                      "DNI",
                      "Nombre_Completo",
                      "saldo",
                      "recuperacion",
                      "recargos",
                      "intereses",
                      "Total_Resultado"
                      ]]
    nuevo_df.columns = ["No. Recibo",
                        "DNI",
                        "Nombre Completo",
                        "SALDO",
                        "RECUPERACION DE SALDOS",
                        "RECARGOS",
                        "INTERESES",
                        "TOTAL",
                        ]

    return nuevo_df


def sumar_ingresos_bomberos_gobernacion(datos: DataFrame):

    # Sumar horizontalmente
    datos["Total_Resultado"] = datos[[
        "saldo",
        "recuperacion"
    ]].sum(axis=1)

    datos["Nombre_Completo"] = (
        datos["Pnombre"].fillna('') + ' ' +
        datos["SNombre"].fillna('') + ' ' +
        datos["PApellido"].fillna('') + ' ' +
        datos["SApellido"].fillna('')
    ).str.replace(r'\s+', ' ', regex=True).str.strip()

    fila_total = {
        "DNI": "",
        "Pnombre": "",
        "SNombre": "",
        "PApellido": "",
        "SApellido": "",
        "saldo": datos["saldo"].sum(),
        "recuperacion": datos["recuperacion"].sum(),
        "NumRecibo": '',
        "Total_Resultado": datos["Total_Resultado"].sum(),
        "Nombre_Completo": "Total",
    }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["NumRecibo",
                      "DNI",
                      "Nombre_Completo",
                      "saldo",
                      "recuperacion",
                      "Total_Resultado"
                      ]]
    nuevo_df.columns = ["No. Recibo",
                        "DNI",
                        "Nombre Completo",
                        "SALDO",
                        "RECUPERACION DE SALDOS",
                        "TOTAL",
                        ]

    return nuevo_df


def sumar_ingresos_generales_depto(datos: DataFrame):

    fila_total = {

        "DeptoDesc": "Total",
        "TotalReciboPagado": datos["TotalReciboPagado"].sum(),
    }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    datos.columns = ["DEPARTAMENTO - UNIDAD",
                     "INGRESOS",
                     ]

    return datos
