import sys
from collections import Counter

def main(ruta_fichero):
    # Lee los dominios contenidos en un fichero
    with open(ruta_fichero, 'r', encoding='utf-8') as f:
        dominios = [line.strip() for line in f if line.strip()]

    # Variables definidas para almacenar las longitudes de los dominios, longitudes de las extensiones y las diferentes extensiones
    longitudes_nombre = []
    longitudes_extension = []
    extensiones = []

    for dom in dominios:
        try:
            # Separamos en dos variables la parte inicial y la extensión
            parte_inicial, extension = dom.rsplit('.', 1)
        except ValueError:
            print(f"Dominio mal formado (sin extensión): {dom}")
            continue

        longitudes_nombre.append(len(parte_inicial))
        longitudes_extension.append(len(extension))
        extensiones.append(extension)

    # Calculo longitud media del nombre
    longitud_media_nombre = sum(longitudes_nombre) / len(longitudes_nombre) if longitudes_nombre else 0.0

    # Calculo longitud media de la extensión
    longitud_media_extension = sum(longitudes_extension) / len(longitudes_extension) if longitudes_extension else 0.0

    # Calculo frecuencia de longitudes del nombre
    contador_longitudes = Counter(longitudes_nombre)

    # Calculo frecuencia de extensiones
    contador_extensiones = Counter(extensiones)

    # Resultados
    print("=== Longitudes de los nombres y su frecuencia ===")
    for length, count in sorted(contador_longitudes.items()):
        print(f"Longitud = {length}: {count} dominios")

    print("\n=== Longitud media del nombre ===")
    print(f"La longitud media (parte antes del punto) es: {longitud_media_nombre:.2f} caracteres.")

    print("\n=== Longitud media de la extensión ===")
    print(f"La longitud media de la extensión es: {longitud_media_extension:.2f} caracteres.")

    print("\n=== Frecuencia de extensiones ===")
    for ext, freq in sorted(contador_extensiones.items()):
        print(f".{ext}: {freq}")

if __name__ == "__main__":
    fichero_dominios = "datos.txt"
    main(fichero_dominios)
