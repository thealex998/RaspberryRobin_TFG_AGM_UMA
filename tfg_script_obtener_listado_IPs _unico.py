import os
import csv
from datetime import datetime

# ============= CONFIGURACIÓN =============
CARPETA_ENTRADA = "/Volumes/Alejandro SSD/TFG/base_datos_bruto_dominios_filtrada"   # Carpeta con CSVs filtrados
FECHA_INICIO    = "2024-02-28 00:00:00"
FECHA_FIN       = "2024-05-29 23:59:59"

rango_inicio = FECHA_INICIO[:10].replace("-", "")
rango_fin    = FECHA_FIN[:10].replace("-", "")
nombre_rango = f"{rango_inicio}-{rango_fin}"

CSV_SALIDA = f"/Volumes/Alejandro SSD/TFG/resultados_ips_unicas_{nombre_rango}.csv"
# =========================================

def parse_fecha(fecha_str):
    formatos = [
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S"
    ]
    for fmt in formatos:
        try:
            return datetime.strptime(fecha_str, fmt)
        except Exception:
            continue
    raise ValueError(f"Fecha no reconocida: {fecha_str}")

fecha_inicio_dt = parse_fecha(FECHA_INICIO)
fecha_fin_dt = parse_fecha(FECHA_FIN)

resultados = set()  # (dominio, ip)

for filename in os.listdir(CARPETA_ENTRADA):
    if not filename.endswith(".csv"):
        continue

    # Limpieza del nombre de dominio
    dominio_base = os.path.splitext(filename)[0]
    if dominio_base.endswith("_filtrado"):
        dominio_base = dominio_base[:-9]
    dominio_limpio = dominio_base.replace('_', '.')

    path_csv = os.path.join(CARPETA_ENTRADA, filename)
    with open(path_csv, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3:
                continue
            # Se usa dominio_limpio para el resultado
            ip, fecha = row[1].strip(), row[2].strip()
            if ip == "0":
                continue  # Salta las IPs igual a 0, por si acaso
            try:
                fecha_dt = parse_fecha(fecha)
            except Exception:
                continue
            if not (fecha_inicio_dt <= fecha_dt <= fecha_fin_dt):
                continue
            resultados.add((dominio_limpio, ip))

# Escritura del CSV final
with open(CSV_SALIDA, 'w', newline='', encoding='utf-8') as f_out:
    f_out.write(f"# Rango analizado: {FECHA_INICIO[:10]} a {FECHA_FIN[:10]}\n")
    writer = csv.writer(f_out)
    writer.writerow(["Dominio", "IP"])
    for dominio, ip in sorted(resultados):
        writer.writerow([dominio, ip])

print(f"\nIPs únicas extraídas y guardadas en: {CSV_SALIDA}")
