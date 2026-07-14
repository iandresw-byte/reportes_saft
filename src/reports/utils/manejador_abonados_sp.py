from pandas import DataFrame


def sumar_mora_abonados_servicios(datos: DataFrame):

    # Sumar horizontalmente
    datos["Total_Resultado"] = datos[[
        "servicio",
        "recuperacion",
        "interes",
        "recargo"
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
    datos["mes_inicial_descripcion"] = datos["mes_inicial"].map(mapa_mes)
    datos["mes_final_descripcion"] = datos["mes_final"].map(mapa_mes)


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
        "CodAbonado": "",
        "CuentaAbonado": "",
        "CtaIngreso": "",
        "NombreCtaIngreso": "",
        "mes_inicial": "",
        "anio_inicial": "",
        "mes_final": "",
        "anio_final": "Total",
        "servicio": datos["servicio"].sum(),
        "recuperacion": datos["recuperacion"].sum(),
        "interes": datos["interes"].sum(),
        "recargo": datos["recargo"].sum(),
        "Total_Resultado": datos["Total_Resultado"].sum(),
        "mes_inicial_descripcion":"",
        "mes_final_descripcion":"",
        "Nombre_Completo": "",
    }

    # Agregar fila al DataFrame
    datos.loc[len(datos)] = fila_total

    nuevo_df = datos[["DNI",
                      "Nombre_Completo",
                      "CodAbonado",
                      "CuentaAbonado",
                      "CtaIngreso",
                      "NombreCtaIngreso",
                      "mes_inicial_descripcion",
                      "anio_inicial",
                      "mes_final_descripcion",
                      "anio_final",
                      "servicio",
                      "recuperacion",
                      "interes",
                      "recargo",
                      "Total_Resultado"
                      ]]
    nuevo_df.columns = ["DNI",
                        "Nombre Completo",
                        "Codigo",
                        "Cuenta",
                        "Cuenta Ingreso",
                        "Nombre Servicio",
                        "Mes Incio Mora",
                        "Anio Inicio Mora",
                        "Mes Fin Mora",
                        "Anio Fin Mora",
                        "Mora Año Actual",
                        "Mora Años Anteriores",
                        "Intereses",
                        "Recargos",
                        "TOTAL",
                        ]

    return nuevo_df