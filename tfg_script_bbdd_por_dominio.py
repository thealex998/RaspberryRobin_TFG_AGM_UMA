import os
import csv
from datetime import datetime
import time  # Para medir el tiempo

CARPETA_PADRE = "/Volumes/Alejandro SSD/TFG/tercera_ejecucion"
CARPETA_SALIDA = "/Volumes/Alejandro SSD/TFG/base_datos_bruto_dominio_todos"

def extrae_fecha(filename):
    filename = filename.replace("/", ":")
    import re
    m = re.match(r"res_csv_iP(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\.csv", filename)
    if m:
        return m.group(1)
    return None

inicio = time.time()  # Inicia la medición de tiempo

# 1. Recoger todas las rutas de los csv de entrada junto a su fecha extraída
csvs_con_fechas = []

for root, dirs, files in os.walk(CARPETA_PADRE):
    for filename in files:
        if not filename.endswith('.csv'):
            continue
        fecha_str = extrae_fecha(filename)
        if not fecha_str:
            continue
        try:
            fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S.%f")
        except Exception:
            continue  # descarta si la fecha no es parseable
        path_csv = os.path.join(root, filename)
        csvs_con_fechas.append((fecha_dt, path_csv, fecha_str))

# 2. Ordenar la lista de rutas por fecha
csvs_con_fechas.sort()  # menor a mayor

# 3. Procesar los archivos ya en orden
files_out = {}
try:
    for fecha_dt, path_csv, fecha_str in csvs_con_fechas:
        with open(path_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) < 2:
                    continue
                dominio, ip = row[0].strip(), row[1].strip()
                dominio_salida = dominio.replace('.', '_')
                nombre_fichero = dominio_salida + ".csv"
                path_salida = os.path.join(CARPETA_SALIDA, nombre_fichero)
                if dominio not in files_out:
                    files_out[dominio] = open(path_salida, 'a', encoding='utf-8')
                fout = files_out[dominio]
                fout.write(f"{dominio},{ip},{fecha_str}\n")
finally:
    for fout in files_out.values():
        fout.close()

fin = time.time()  # Finaliza la medición de tiempo
print(f"Tiempo total de ejecución: {fin - inicio:.2f} segundos")
