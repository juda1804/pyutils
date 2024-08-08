import pandas as pd

# Leer el archivo de texto
file_path = '/home/juan-cadavid/PycharmProjects/util-functions/convert-to-xls/REPOR333.TXT'


# Inicializar listas para almacenar los datos
codigo = []
descripcion = []
costo_unitario = []
existencia = []
unidades = []
costo_existencia = []
precio_publico = []
precio_x_mayor = []
costo_flete_otros = []
errores = []

# Función para convertir y formatear los costos
def process_cost(value):
    try:
        # Remover los dos últimos dígitos
        value = value[:-3]
        # Reemplazar comas por puntos y convertir a float
        return float(value.replace(',', '').replace('.', ''))
    except ValueError:
        return None

# Leer el archivo en modo binario, reemplazar caracteres problemáticos y decodificar
with open(file_path, 'rb') as file:
    content = file.read()
    content = content.replace(b'\xc2', b'').replace(b'\xa2', b'').decode('latin-1')

# Dividir el contenido en líneas
lines = content.splitlines()

# Procesar las líneas del archivo
for line in lines[6:]:  # Saltar las primeras 6 líneas del encabezado
    if line.strip():
        try:
            parts = line.split()
            if len(parts) >= 8:  # Asegurar que la línea tenga al menos 8 partes
                codigo.append(parts[0])
                descripcion.append(' '.join(parts[1:-7]))
                costo_unitario.append(process_cost(parts[-7]))
                existencia.append(parts[-6])
                unidades.append(parts[-5])
                costo_existencia.append(process_cost(parts[-4]))
                precio_publico.append(process_cost(parts[-3]))
                precio_x_mayor.append(process_cost(parts[-2]))
                costo_flete_otros.append(process_cost(parts[-1]))
            else:
                raise ValueError(f"Línea con número insuficiente de partes {line}")
        except Exception as e:
            errores.append(f"Error en la línea: {line}\nError: {e}")

# Verificar que todas las listas tengan la misma longitud
longitudes = [len(codigo), len(descripcion), len(costo_unitario), len(existencia), len(unidades), len(costo_existencia), len(precio_publico), len(precio_x_mayor), len(costo_flete_otros)]
min_length = min(longitudes)
if any(length != min_length for length in longitudes):
    print("Advertencia: No todas las listas tienen la misma longitud. Truncando listas para igualarlas.")
    codigo = codigo[:min_length]
    descripcion = descripcion[:min_length]
    costo_unitario = costo_unitario[:min_length]
    existencia = existencia[:min_length]
    unidades = unidades[:min_length]
    costo_existencia = costo_existencia[:min_length]
    precio_publico = precio_publico[:min_length]
    precio_x_mayor = precio_x_mayor[:min_length]
    costo_flete_otros = costo_flete_otros[:min_length]

# Crear un DataFrame de pandas
df = pd.DataFrame({
    'Código': codigo,
    'Descripción': descripcion,
    'Costo unitario': costo_unitario,
    'Existencia': existencia,
    'Unidades': unidades,
    'Costo existencia': costo_existencia,
    'Precio Público': precio_publico,
    'Precio x Mayor': precio_x_mayor,
    'Costo+Flete+otros': costo_flete_otros
})

# Guardar el DataFrame en un archivo Excel
output_path = 'reporte_productos.xlsx'
df.to_excel(output_path, index=False)

# Guardar el archivo de errores si hay errores
if errores:
    with open('errores.txt', 'w', encoding='utf-8') as error_file:
        for error in errores:
            error_file.write(f"{error}\n")

print(f'Archivo Excel guardado en: {output_path}')
if errores:
    print(f'Se encontraron errores. Revisa el archivo errores.txt para más detalles.')