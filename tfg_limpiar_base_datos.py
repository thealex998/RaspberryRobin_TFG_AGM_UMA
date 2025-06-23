import csv
from datetime import datetime, timedelta
import os

# === CONFIGURACIÓN ===
CARPETA_ORIGEN = "/Volumes/Alejandro SSD/TFG/base_datos_bruto_dominio_todos/"   # Carpeta con CSVs originales
CARPETA_DESTINO = "/Volumes/Alejandro SSD/TFG/base_datos_bruto_dominios_filtrada/"                         # Carpeta para los CSVs limpios

def parse_fecha(fecha_str):
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(fecha_str, fmt)
        except Exception:
            continue
    raise ValueError(f"Fecha no reconocida: {fecha_str}")

def construir_nombre_salida(filename, carpeta_destino):
    base = os.path.splitext(filename)[0]
    return os.path.join(carpeta_destino, f"{base}_filtrado.csv")

def limpiar_csv(path_csv, path_limpio):
    with open(path_csv, newline='', encoding='utf-8') as f_in:
        reader = list(csv.reader(f_in))
    if not reader:  # Salta ficheros vacíos
        return

    reader.sort(key=lambda row: parse_fecha(row[2].strip()))

    filas_filtradas = []
    i = 0
    n = len(reader)
    prev_ip = None

    while i < n:
        dominio, ip, fecha = reader[i][0].strip(), reader[i][1].strip(), reader[i][2].strip()

        # Caso IP distinta de "0"
        if ip != "0":
            if ip != prev_ip:
                filas_filtradas.append([dominio, ip, fecha])
                prev_ip = ip
            i += 1
            continue

        # --- Bloque de "0" ---
        bloque_inicio = i
        while i + 1 < n and reader[i + 1][1].strip() == "0":
            i += 1
        bloque_fin = i

        fecha_inicio = parse_fecha(reader[bloque_inicio][2].strip())
        fecha_fin = parse_fecha(reader[bloque_fin][2].strip())
        duracion = fecha_fin - fecha_inicio

        if duracion >= timedelta(hours=6):
            filas_filtradas.append([dominio, "0", reader[bloque_inicio][2].strip()])
            prev_ip = "0"
        # Si dura menos, NO se añade ninguna fila de ese bloque

        i = bloque_fin + 1

    with open(path_limpio, 'w', newline='', encoding='utf-8') as f_out:
        writer = csv.writer(f_out)
        writer.writerows(filas_filtradas)

    print(f"✓ {os.path.basename(path_limpio)} ({len(filas_filtradas)} filas)")

if __name__ == "__main__":
    if not os.path.isdir(CARPETA_ORIGEN):
        print(f"Error: la carpeta de origen no existe: {CARPETA_ORIGEN}")
    else:
        os.makedirs(CARPETA_DESTINO, exist_ok=True)
        archivos = [f for f in os.listdir(CARPETA_ORIGEN) if f.endswith('.csv')]
        print(f"Procesando {len(archivos)} archivos...\n")
        for nombre_csv in archivos:
            path_csv = os.path.join(CARPETA_ORIGEN, nombre_csv)
            path_limpio = construir_nombre_salida(nombre_csv, CARPETA_DESTINO)
            try:
                limpiar_csv(path_csv, path_limpio)
            except Exception as e:
                print(f"[ERROR] {nombre_csv}: {e}")
        print("\nCompletado.")
