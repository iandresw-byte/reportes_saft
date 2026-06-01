import flet as ft
from pandas import DataFrame
from src.models.apremio_models import EstadoApremio
from src.ui.components.ui_colors import color_texto
from src.ui.components.ui_text import create_text_paginacion, create_text_table
text_color = color_texto()


def color_estado_proceso(estado: str):
    if estado == EstadoApremio.PRONTO_VENCE.value:
        return ft.Colors.AMBER_700
    elif estado == EstadoApremio.ENTREGADO.value:
        return ft.Colors.GREEN_700
    elif estado == EstadoApremio.GENERADO.value:
        return ft.Colors.BLUE_700
    elif estado == EstadoApremio.VENCIDO.value:
        return ft.Colors.RED_700
    elif estado == EstadoApremio.NO_GENERADO.value:
        return ft.Colors.WHITE70
    elif estado == EstadoApremio.ANULADO.value:
        return ft.Colors.RED_700
    else:
        return ft.Colors.PINK_700


def table_requeridos(vista, df: DataFrame, pagina=1, filas_por_pagina=10) -> ft.DataTable:
    def editar(e):
        fila = e.control.data
        vista.abrir_modal_editar(fila)

    def eliminar(e):
        id_doc = e.control.data
        vista.abrir_modal_eliminar(id_doc)

    def ver(e):
        fila = e.control.data
        vista.abrir_modal_ver(fila)

    def obtener_pagina(df, pagina=1, filas_por_pagina=10):
        inicio = (pagina - 1) * filas_por_pagina
        fin = inicio + filas_por_pagina
        if isinstance(df, DataFrame):
            if not df.empty:
                return df.iloc[inicio:fin]

    rows = []
    df_pagina = obtener_pagina(df, pagina, filas_por_pagina)
    if df is not None:
        for _, row in df_pagina.iterrows():
            color_fecha_entrega = color_estado_proceso(row["Estado"])
            if row["Estado"] == EstadoApremio.PRONTO_VENCE.value:
                str_fecha_entrega = f"{int(30 - row["DiasDesdeGenerado"])} dias para Vencer"
            elif row["Estado"] == EstadoApremio.VENCIDO.value:
                str_fecha_entrega = f"Reinicie el Proceso"
            else:
                str_fecha_entrega = row["FechaFormateadaEntrega"]

            if len(row["Observacion"]) > 20:
                observacion = f"{row["Observacion"][:15]} mas..."
            else:
                observacion = row["Observacion"]
            editar_visble = True
            eliminar_visible = True
            if row["Estado"] == 'Entregado':
                editar_visble = False
                eliminar_visible = False

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(create_text_table(
                            str(row["IdDocumento"]))),
                        ft.DataCell(create_text_table(row["DNI_Formateado"])),
                        ft.DataCell(create_text_table(row["NombreCompleto"]),),
                        ft.DataCell(create_text_table(
                            str(row["Monto_ini_formateado"]))),
                        ft.DataCell(create_text_table(
                            row["TipoDocDescripcion"])),
                        ft.DataCell(create_text_table(
                            row["Estado"])),
                        ft.DataCell(create_text_table(
                            row["FechaFormateadaGenerada"])),
                        ft.DataCell(create_text_table(
                            str_fecha_entrega, color_fecha_entrega)),
                        ft.DataCell(create_text_table(observacion)),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.VISIBILITY,
                                        tooltip="Ver",
                                        data=row.to_dict(),
                                        on_click=ver,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        tooltip="Editar",
                                        data=row.to_dict(),
                                        on_click=editar,
                                        visible=editar_visble,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        tooltip="Anular Proceso",
                                        data=row["IdDocumento"],
                                        on_click=eliminar,
                                        icon_color="red",
                                        visible=eliminar_visible,
                                    ),
                                ],
                                spacing=5,
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ),
                    ]
                )
            )

    return ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("No.")),
            ft.DataColumn(label=ft.Text("Identidad")),
            ft.DataColumn(label=ft.Text("Nombre")),
            ft.DataColumn(label=ft.Text("Deuda"),
                          numeric=True,
                          tooltip="Monto de Mora Requerido",),
            ft.DataColumn(label=ft.Text("Tipo Documento")),
            ft.DataColumn(label=ft.Text("Estado")),
            ft.DataColumn(label=ft.Text("Fecha Generado")),
            ft.DataColumn(label=ft.Text("Fecha Entregado")),
            ft.DataColumn(label=ft.Text("Observaciones")),
            ft.DataColumn(label=ft.Text("Acciones")),
        ],

        rows=rows,
        expand=True
    )


def controles_paginacion(vista, df, pagina_actual, filas_por_pagina):
    tamanio = 0
    if isinstance(df, DataFrame):
        tamanio = len(df)
    total_paginas = (tamanio + filas_por_pagina - 1) // filas_por_pagina
    return ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color=text_color,
                disabled=pagina_actual == 1,
                on_click=lambda e: vista.cambiar_pagina(pagina_actual - 1)
            ),
            create_text_paginacion(
                f"Página {pagina_actual} de {total_paginas}"),
            ft.IconButton(
                icon=ft.Icons.ARROW_FORWARD,
                icon_color=text_color,
                disabled=pagina_actual == total_paginas,
                on_click=lambda e: vista.cambiar_pagina(pagina_actual + 1)
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )


def table_identifiacion_top(vista, df: DataFrame, pagina=1, filas_por_pagina=10) -> ft.DataTable:
    def ver(e):
        fila = e.control.data
        vista.generar_apremio_pdf_individual(fila)

    rows = []
    if isinstance(df, DataFrame):
        if not df.empty:
            if df is not None:
                for index, row in df.iterrows():
                    rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(create_text_table(
                                    str(index))),
                                ft.DataCell(create_text_table(row["dni"])),
                                ft.DataCell(create_text_table(row["nombre"]),),
                                ft.DataCell(create_text_table(
                                    str(row["periodo"]))),
                                ft.DataCell(create_text_table(row["mora"])),
                                ft.DataCell(
                                    ft.Row(
                                        [
                                            ft.IconButton(
                                                icon=ft.Icons.VISIBILITY,
                                                tooltip="Ver",
                                                data=row["dni"],
                                                on_click=ver,
                                            ),
                                        ],
                                        spacing=5,
                                        alignment=ft.MainAxisAlignment.CENTER
                                    )
                                ),
                            ]
                        )
                    )

    return ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("No.")),
            ft.DataColumn(label=ft.Text("DNI")),
            ft.DataColumn(label=ft.Text("Nombre")),
            ft.DataColumn(label=ft.Text("Facturado Hasta")),
            ft.DataColumn(label=ft.Text("Deuda"),
                          numeric=True,
                          tooltip="Monto de Mora Requerido",),
            ft.DataColumn(label=ft.Text("Acciones")),
        ],

        rows=rows,
        expand=True
    )


def table_identifiacion_top_ics(vista, df: DataFrame, pagina=1, filas_por_pagina=10) -> ft.DataTable:
    def ver(e):
        fila = e.control.data
        vista.abrir_modal_ver(fila)

    def obtener_pagina(df, pagina=1, filas_por_pagina=10):
        inicio = (pagina - 1) * filas_por_pagina
        fin = inicio + filas_por_pagina
        if isinstance(df, DataFrame):
            if not df.empty:
                return df.iloc[inicio:fin]

    rows = []
    if isinstance(df, DataFrame):
        if df is not None:
            for index, row in df.iterrows():
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(create_text_table(
                                str(index))),
                            ft.DataCell(create_text_table(row["rtm"])),
                            ft.DataCell(create_text_table(
                                row["establecimiento"])),
                            ft.DataCell(create_text_table(row["dni"])),
                            ft.DataCell(create_text_table(row["nombre"])),
                            ft.DataCell(create_text_table(row["periodo"])),
                            ft.DataCell(create_text_table(row["mora"]),),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.VISIBILITY,
                                            tooltip="Ver",
                                            data=row.to_dict(),
                                            on_click=ver,
                                        ),
                                    ],
                                    spacing=5,
                                    alignment=ft.MainAxisAlignment.CENTER
                                )
                            ),
                        ]
                    )
                )

    return ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("No.")),
            ft.DataColumn(label=ft.Text("R.T.M.")),
            ft.DataColumn(label=ft.Text("Nombre Establecimiento")),
            ft.DataColumn(label=ft.Text("DNI")),
            ft.DataColumn(label=ft.Text("Nombre Propietario")),
            ft.DataColumn(label=ft.Text("Perioido Facturado")),
            ft.DataColumn(label=ft.Text("Mora"),
                          numeric=True,
                          tooltip="Monto de Mora Requerido",),
            ft.DataColumn(label=ft.Text("Acciones")),
        ],

        rows=rows,
        expand=True
    )
