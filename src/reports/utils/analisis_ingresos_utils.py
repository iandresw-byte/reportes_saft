
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter, range_boundaries
border = Border(
                left=Side(style="thin"), right=Side(style="thin"),
                top=Side(style="thin"), bottom=Side(style="thin")
            )
aling_centrado = Alignment(horizontal="center", vertical="center")
align_left = Alignment(horizontal="left", vertical="center")
    
def color_columa_diferencia(ultima_fila, ws, columna):
    for row in range(6, ultima_fila + 1):
        cell = ws[f"{columna}{row}"]          # Celda actual en columna J
        valor = float(str(cell.value).replace(",",""))
        if valor is None:
            continue
        if valor < 0:
            color = "FF7F7F"
        elif valor >= 0:
            color = "00B050"
        # Aplicar color
        cell.fill = PatternFill(
            start_color=color, end_color=color, fill_type="solid")

def formato_titulo(ws,valor_celda,fila):
    aligneacion = Alignment(horizontal="center", vertical="center")
    title_font = Font(size=16, bold=True)
    celda = fila[:2]
    if len(fila)>6:
        celda = fila[:3]
    ws.merge_cells(fila)
    ws[celda] = valor_celda
    ws[celda].alignment = aligneacion
    ws[celda].font = title_font

def formato_fecha(ws,valor_celda,fila):
    aligneacion = Alignment(horizontal="center", vertical="center")
    date_font = Font(size=12, italic=True)
    celda = fila[:2]
    if len(fila)>6:
        celda = fila[:3]
    ws.merge_cells(fila)
    ws[celda] = valor_celda
    ws[celda].alignment = aligneacion
    ws[celda].font = date_font

def formato_mes(ws,valor_mes,fila):
    aligneacion = Alignment(horizontal="center", vertical="center")
    title_mes_font = Font(size=13, bold=True)
    
    celda = fila[:2]
    if len(fila)>6:
        celda = fila[:3]
    ws.merge_cells(fila)
    ws[celda] = valor_mes
    ws[celda].alignment = aligneacion
    ws[celda].font = title_mes_font

def formato_titulo_columna(ws, columnas,fila_actual):
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    col_value = 0
    for col in range(1, len(columnas) + 1):
        c = ws.cell(row=fila_actual, column=col, value=columnas[col_value])
        c.fill = header_fill
        c.font = header_font
        c.alignment = aling_centrado
        c.border = border
        col_value += 1

def formato_celdas_moneda(ws, primera_fila=5, ultima_fila=35, columna_max=41, rango = "C5:AO35"):
    min_col, _, max_col, _= range_boundaries(rango)
    for row in ws.iter_rows(min_row=primera_fila, max_row=ultima_fila, max_col=columna_max):
        for cell in row:
            cell.border = border
            if cell.column in (1, 2):  # Columnas A y B
                cell.alignment = align_left
                cell.number_format = "#,##0"

            elif min_col <= cell.column <= max_col:
                cell.number_format = '"L" #,##0.00'

def ajuste_automatico_columnas(ws):
    for col in ws.columns:
        max_length = 0
        column = col[0].column  # número de columna
        column_letter = get_column_letter(column)
        for cell in col[4:]:
            try:
                if cell.value:
                    length = len(str(cell.value))
                    if length > max_length:
                        max_length = length
            except:
                pass
        adjusted_width = max_length + 2  # un pequeño margen
        ws.column_dimensions[column_letter].width = adjusted_width
    
    