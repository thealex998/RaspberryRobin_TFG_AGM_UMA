import csv
import os
from datetime import datetime

# ============= CONFIGURACIÓN =============
CARPETA_ENTRADA = "/Volumes/Alejandro SSD/TFG/base_datos_bruto_dominios_filtrada"   # Carpeta con CSVs filtrados
FECHA_INICIO    = "2024-02-28 00:00:00"
FECHA_FIN       = "2024-05-29 23:59:59"

# Extrae solo la fecha (YYYYMMDD) para el nombre del fichero
rango_inicio = FECHA_INICIO[:10].replace("-", "")
rango_fin    = FECHA_FIN[:10].replace("-", "")
nombre_rango = f"{rango_inicio}-{rango_fin}"

CSV_SALIDA   = f"/Volumes/Alejandro SSD/TFG/resultados_tiempo_medio_cambio_{nombre_rango}.csv"
# =========================================

def parse_fecha(fecha_str):
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(fecha_str, fmt)
        except Exception:
            continue
    raise ValueError(f"Fecha no reconocida: {fecha_str}")

inicio_dt = parse_fecha(FECHA_INICIO)
fin_dt = parse_fecha(FECHA_FIN)

resultados = []

for nombre_csv in sorted(f for f in os.listdir(CARPETA_ENTRADA) if f.endswith('.csv')):
    path_csv = os.path.join(CARPETA_ENTRADA, nombre_csv)
    ips = []
    fechas = []

    with open(path_csv, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3:
                continue
            ip = row[1].strip()
            fecha = parse_fecha(row[2].strip())

            # Omitimos todo lo que está antes del rango
            if fecha < inicio_dt:
                continue

            # Si ya pasamos el rango, rompemos el bucle
            if fecha > fin_dt:
                break

            ips.append(ip)
            fechas.append(fecha)

    if len(ips) < 2:
        continue

    tiempos = []
    prev_fecha = fechas[0]
    prev_ip = ips[0]
    for ip, fecha in zip(ips[1:], fechas[1:]):
        if ip != prev_ip:
            horas = (fecha - prev_fecha).total_seconds() / 3600.0
            tiempos.append(horas)
            prev_fecha = fecha
            prev_ip = ip

    if tiempos:
        # Limpieza del nombre: elimina _filtrado y lo convierte a dominio real
        dominio_base = os.path.splitext(nombre_csv)[0]
        if dominio_base.endswith("_filtrado"):
            dominio_base = dominio_base[:-9]
        dominio = dominio_base.replace('_', '.')
        resultados.append([dominio, round(sum(tiempos) / len(tiempos), 2)])

with open(CSV_SALIDA, 'w', newline='', encoding='utf-8') as fout:
    fout.write(f"# Rango analizado: {FECHA_INICIO[:10]} a {FECHA_FIN[:10]}\n")
    writer = csv.writer(fout)
    writer.writerow(["Dominio", "MediaCambioHoras"])
    for fila in sorted(resultados, key=lambda x: x[0]):
        writer.writerow(fila)

print(f"Resultados guardados en: {CSV_SALIDA}")
