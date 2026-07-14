from pandas import DataFrame


def sumar_establecimientos_actividad(datos: DataFrame, tipo_rpt):

    # Sumar horizontalmente
    datos["Total_Resultado"] = datos[[
        "MoraIndusActual",
        "MoraComerActual",
        "MoraServicActual",
        "MoraAniosAnte_I",
        "MoraAniosAnte_C",
        "MoraAniosAnte_S",
        "PermisoOpetacion",
        "Intereses",
        "Recargos",
        "Multas",
        "Descuentos"
    ]].sum(axis=1)

    datos["Otros_Saldo"] = datos["Saldo_Sumado"].fillna(
        0) - datos["Total_Resultado"].fillna(0)

    datos["Total_Impuesto"] = datos[[
        "MoraIndusActual",
        "MoraComerActual",
        "MoraServicActual",
        "MoraAniosAnte_I",
        "MoraAniosAnte_C",
        "MoraAniosAnte_S",
    ]].sum(axis=1)

    datos["ImpuestoActual"] = datos[[
        "MoraIndusActual",
        "MoraComerActual",
        "MoraServicActual",
    ]].sum(axis=1)

    datos["RecuperacionSaldo"] = datos[[
        "MoraAniosAnte_I",
        "MoraAniosAnte_C",
        "MoraAniosAnte_S",
    ]].sum(axis=1)


    

    datos["Total_Otros"] = datos[[
        "PermisoOpetacion",
        "Intereses",
        "Recargos",
        "Multas",
        "Descuentos",
    ]].sum(axis=1)

    mapa_mes = {
                1: "Enero",
                2: "Febrero",
                3: "Marzo",
                4: "Abril",
                5: "Mayo",
                6: "Junio",
                7: "Julio",
                8: "Agosto",
                9: "Septiembre",
                10: "Octubre",
                11: "Noviembre",
                12: "Diciembre",
            }
    datos["mes_inicial_descripcion"] = (
    datos["mes_inicial"].map(mapa_mes)
    + "-"
    + datos["anio_inicial"].astype(str)
    )
    datos["mes_final_descripcion"] = (
    datos["mes_final"].map(mapa_mes)
    + "-"
    + datos["anio_final"].astype(str)
    )
    datos["Nombre_Completo"] = (
        datos["PNombre"].fillna('') + ' ' +datos["SNombre"].fillna('') + ' ' +
        datos["PApellido"].fillna('') + ' ' +
        datos["SApellido"].fillna('')
    ).str.replace(r'\s+', ' ', regex=True).str.strip()

    fila_total = {
        "rtm": "",
        "Establecimiento": "",
        "DNI": "",
        "PNombre": "",
        "SNombre": "",
        "PApellido": "",
        "SApellido": "",
        "CodActividad": "",
        "Direccion": "",
        "Telefono": "",
        #"NombreCtaIngreso": "",
        "mes_inicial": "",
        "anio_inicial": "",
        "mes_final": "",
        "anio_final": "",
        "MoraIndusActual": datos["MoraIndusActual"].sum(),
        "MoraComerActual": datos["MoraComerActual"].sum(),
        "MoraServicActual": datos["MoraServicActual"].sum(),
        "MoraAniosAnte_I": datos["MoraAniosAnte_I"].sum(),
        "MoraAniosAnte_C": datos["MoraAniosAnte_C"].sum(),
        "MoraAniosAnte_S": datos["MoraAniosAnte_S"].sum(),
        "PermisoOpetacion": datos["PermisoOpetacion"].sum(),
        "Intereses": datos["Intereses"].sum(),
        "Recargos": datos["Recargos"].sum(),
        "Multas": datos["Multas"].sum(),
        "Descuentos": datos["Descuentos"].sum(),
        "Total_Resultado": datos["Total_Resultado"].sum(),
        "Otros_Saldo": datos["Otros_Saldo"].sum(),
        "Total_Impuesto": datos["Total_Impuesto"].sum(),
        "ImpuestoActual": datos["ImpuestoActual"].sum(),
        "RecuperacionSaldo": datos["RecuperacionSaldo"].sum(),
        "Total_Otros": datos["Total_Otros"].sum(),
        "mes_inicial_descripcion":"",
        "mes_final_descripcion":"Total",
        "Nombre_Completo": "",
    }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total
    if tipo_rpt == "excel":
        nuevo_df = datos[[
                        "rtm",
                        "Establecimiento",
                        "DNI",
                        "Nombre_Completo",
                        "CodActividad",
                        "Direccion",
                        "Telefono",
                        "mes_inicial_descripcion",
                        "mes_final_descripcion",
                        "MoraIndusActual",
                        "MoraComerActual",
                        "MoraServicActual",
                        "MoraAniosAnte_I",
                        "MoraAniosAnte_C",
                        "MoraAniosAnte_S",
                        "PermisoOpetacion",
                        "Intereses",
                        "Recargos",
                        "Multas",
                        "Descuentos",
                        "Total_Otros",
                        "Total_Resultado"
                        ]]
        nuevo_df.columns = ["Registro Tributario Municipal (RTM)",
                                "Establecimiento",
                                "DNI",
                                "Comerciante",
                                "Cuenta Actividad Economica",
                                "Direccion",
                                "Telefono",
                                "Inicio Saldos",
                                "Facturado Hasta",
                                "Saldo Año Actual Industria",
                                "Saldo Año Actual Comercio",
                                "Saldo Año Actual Servicio",
                                "Saldo Años Anteriores Industria",
                                "Saldo Años Anteriores Comercio",
                                "Saldo Años Anteriores Servicio",
                                "Saldos Permiso de Operacion",
                                "Intereses",
                                "Recargos",
                                "Multas",
                                "Descuentos",
                                "Otros Saldos",
                                "Total" ]

    elif tipo_rpt == "pdf":
        nuevo_df = datos[["rtm",
                        "Establecimiento",
                        "Nombre_Completo",
                        "CodActividad",
                        "Direccion",
                        "Telefono",
                        "ImpuestoActual",
                        "RecuperacionSaldo",
                        "Total_Otros",
                        "Total_Resultado"
                        ]]
        nuevo_df.columns = ["Registro Tributario Municipal (RTM)",
                            "Nombre Establecimiento",
                            "Comerciante",
                            "Cuenta Actividad Economica",
                            "Direccion Establecimiento",
                            "Telefono",
                            "Impuesto Año Actual",
                            "Impuesto Años Anteriores",
                            "Otros Saldos",
                            "TOTAL",
                            ]

        
    return nuevo_df