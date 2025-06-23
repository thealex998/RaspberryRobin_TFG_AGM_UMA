import sys
from collections import Counter

def main(ruta_fichero):
    # Lee los dominios contenidos en un fichero
    with open(ruta_fichero, 'r', encoding='utf-8') as f:
        dominios = [line.strip() for line in f if line.strip()]

    # Variables definidas para almacenar las longitudes de los dominios y las diferentes extensiones
    longitudes = []
    extensiones = []

    for dom in dominios:
        # Separamos en dos variables la longitud del nombre del dominio y las extensiones
        parte_inicial, extension = dom.rsplit('.', 1)
        longitudes.append(len(parte_inicial))
        extensiones.append(extension)

    contador_longitudes = Counter(longitudes)

    # Calculo longitud media
    longitud_media = sum(longitudes) / len(longitudes) if longitudes else 0.0

    # Calculo frecuencia de cada extension
    contador_extensiones = Counter(extensiones)

    print("=== Longitudes y su frecuencia ===")
    for length, count in sorted(contador_longitudes.items()):
        print(f"Longitud = {length}: {count} dominios")

    print("\n=== Longitud media ===")
    print(f"La longitud media (parte antes del punto) es: {longitud_media:.2f}")

    print("\n=== Frecuencia de extensiones ===")
    for ext, freq in sorted(contador_extensiones.items()):
        print(f".{ext}: {freq}")

if __name__ == "__main__":
    fichero_dominios = "datos.txt"
    main(fichero_dominios)
