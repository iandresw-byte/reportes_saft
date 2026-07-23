from decimal import ROUND_HALF_UP, Decimal

import pandas as pd




def limpar_bienes_inmuebles(data_mora :pd.DataFrame):
    def decimal_preciso(valor):
        if valor is None:
            valor = 0
        return Decimal(str(valor)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

    print(data_mora.columns)
    data_mora['bi'] = data_mora['bi'].apply(decimal_preciso) # type: ignore
    data_mora['ip'] = data_mora['ip'].apply(decimal_preciso) # type: ignore
    data_mora['ind'] = data_mora['ind'].apply(decimal_preciso) # type: ignore
    data_mora['com'] = data_mora['com'].apply(decimal_preciso) # type: ignore
    data_mora['ser'] = data_mora['ser'].apply(decimal_preciso) # type: ignore
    data_mora['pecuario'] = data_mora['pecuario'].apply(decimal_preciso) # type: ignore
    data_mora['extraccion'] = data_mora['extraccion'].apply(decimal_preciso) # type: ignore
    data_mora['selectivo'] = data_mora['selectivo'].apply(decimal_preciso) # type: ignore
    data_mora['servicios'] = data_mora['servicios'].apply(decimal_preciso) # type: ignore
    data_mora['tasas'] = data_mora['tasas'].apply(decimal_preciso) # type: ignore
    data_mora['multas'] = data_mora['multas'].apply(decimal_preciso) # type: ignore
    data_mora['otros_ingresos'] = data_mora['otros_ingresos'].apply(decimal_preciso) # type: ignore
    data_mora['recargos'] = data_mora['recargos'].apply(decimal_preciso) # type: ignore
    data_mora['descuentos'] = data_mora['descuentos'].apply(decimal_preciso) # type: ignore
    data_mora['recuperacion'] = data_mora['recuperacion'].apply(decimal_preciso) # type: ignore
    data_mora['recuperacionbi'] = data_mora['recuperacionbi'].apply(decimal_preciso) # type: ignore
    data_mora['recuperacionTasas'] = data_mora['recuperacionTasas'].apply(decimal_preciso) # type: ignore
    data_mora['recuperacionSp'] = data_mora['recuperacionSp'].apply(decimal_preciso) # type: ignore
    data_mora['intereses'] = data_mora['intereses'].apply(decimal_preciso) # type: ignore
    data_mora['total'] = data_mora['total'].apply(decimal_preciso) # type: ignore
                                          
    data_mora["Total_Fila"]= data_mora[[ "bi",
        "servicios",
        "tasas",
        "multas",
        "recargos",
        "recuperacionbi",
        "recuperacionTasas",
        "recuperacionSp",
        "intereses",
        "descuentos",
        "otros_ingresos",
        ]].sum(axis=1)
    

    data_mora["Otros"] = data_mora["total"].fillna( 0) - data_mora["Total_Fila"].fillna(0)
    data_mora["Otros"] = data_mora['Otros'].apply(decimal_preciso) # type: ignore
    print(data_mora.columns)

    print(data_mora[['Total_Fila', 'Otros', 'total']])