from src.repositories.registro_unico_repository import RegistroUnicoRepository
import pandas as pd

class RegistroUnicoService:
    def __init__(self, conexion):
        self.repository = RegistroUnicoRepository(conexion)

    def getGravable(
        self,
        anio: str,
        impuesto: float,
        ubicacion: int,
        tasas: dict
    ) -> float:

        if ubicacion == 1:
            tasa = float(tasas["TasaBIUrbana"])
        else:
            tasa = float(tasas["TasaBIRural"])

        if tasa == 0:
            return 0.0

        return impuesto / tasa * 1000.0
    


    def obtener_ruc(self, identidad):
        data_pagos_res = self.repository.obtener_registro_unico_gob(identidad)
        data_declaraciones_bi = (
            self.repository.obtener_declaraciones_bienes_inmuebles(identidad)
        )
        data_declaraciones_ics = (
                    self.repository.obtener_declaraciones_industria_comercio(identidad)
                )
        df_declara_ics = pd.DataFrame(data_declaraciones_ics)
        df_aval = pd.DataFrame(data_declaraciones_bi)

        df_aval = (
            df_aval
            .sort_values(["CatClv", "Periodo"], ascending=[True, False])
        )

        df_declara_ics = (
                    df_declara_ics
                    .sort_values(["rtm", "Periodo"], ascending=[True, False])
                )
        # =====================================================
        # CARGAR TASAS UNA SOLA VEZ POR CADA AÑO
        # =====================================================

        anios = df_aval["Periodo"].dropna().unique()

        tasas_por_anio = {}

        for anio in anios:
            anio = str(int(anio))

            tasas_por_anio[anio] = self.repository.obtener_tasas(
                anio=anio
            )

        # =====================================================
        # CALCULAR GRAVABLE
        # =====================================================

        df_aval["Gravable"] = df_aval.apply(
            lambda fila: self.getGravable(
                anio=str(int(fila["Periodo"])),
                impuesto=float(fila["Impuesto"]),
                ubicacion=int(fila["Ubicacion"]),
                tasas=tasas_por_anio[str(int(fila["Periodo"]))]
            ),
            axis=1
        )

        # =====================================================
        # CREAR SLOT
        # =====================================================

        df_aval["slot"] = (
            df_aval
            .groupby("CatClv")
            .cumcount() + 1
        )

        df_declara_ics["slot"] = (
                    df_declara_ics
                    .groupby("rtm")
                    .cumcount() + 1
                )
        

        df_aval = df_aval[df_aval["slot"] <= 5]
        df_declara_ics = df_declara_ics[df_declara_ics["slot"] <= 5]

        # =====================================================
        # PIVOT
        # =====================================================

        pivot_aval = df_aval.pivot(
            index=["CatClv", "NombreBarrio"],
            columns="slot",
            values=["Periodo", "Impuesto", "Gravable"]
        )

        pivot_declara_ics = df_declara_ics.pivot(
                    index=["rtm", "NombreBarrio"],
                    columns="slot",
                    values=["Periodo", "Impuesto", "Gravable"]
                )

        # =====================================================
        # APLANAR COLUMNAS
        # =====================================================

        pivot_aval.columns = [
            f"{campo}{slot}"
            for campo, slot in pivot_aval.columns
        ]
        pivot_declara_ics.columns = [
                    f"{campo}{slot}"
                    for campo, slot in pivot_declara_ics.columns
                ]
        

        pivot_aval = pivot_aval.reset_index()
        pivot_declara_ics = pivot_declara_ics.reset_index()

        # =====================================================
        # ASEGURAR LAS 5 POSICIONES
        # =====================================================

        columnas = ["CatClv", "NombreBarrio"]

        for i in range(1, 6):
            columnas.extend([
                f"Periodo{i}",
                f"Impuesto{i}",
                f"Gravable{i}"
            ])

        pivot_aval = pivot_aval.reindex(columns=columnas)

        columnas = ["rtm", "NombreBarrio" ]
        
        for i in range(1, 6):
            columnas.extend([
                f"Periodo{i}",
                f"Impuesto{i}",
                f"Gravable{i}"
            ])
        
        pivot_declara_ics = pivot_declara_ics.reindex(columns=columnas)
        

        print("=== Grilla Bienes Inmuebles ===")
        print(pivot_aval)
        print(pivot_declara_ics)
        contribuyente = self.repository.obtener_contribuyente(identidad)
        if contribuyente:
            datos = {'dni': contribuyente['DNI'],
                                'nombre': contribuyente['Pnombre'] + ' ' + contribuyente['SNombre'] + ' ' + contribuyente['PApellido'] + ' ' + contribuyente['SApellido'],
                                'direccion': contribuyente['Direccion'],
                                'clave_catastro': contribuyente['ClaveCatastro'],
                                "datos_pagos":data_pagos_res,
                                "declaraciones_bi": pivot_aval,
                                "declaraciones_ics": pivot_declara_ics,
                                }
        else:
            datos = None
        if not datos:
            raise ValueError(
                f"Datos del contribuyente con la Identidad: {identidad}")
        return datos


