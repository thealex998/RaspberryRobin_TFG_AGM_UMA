from collections import Counter


def leer_dominios_desde_txt(ruta_fichero):
    """
    Lee dominios desde un archivo de texto.
    Cada línea debe contener un dominio.
    """
    with open(ruta_fichero, 'r', encoding='utf-8') as f:
        dominios = [line.strip() for line in f if line.strip()]
    return dominios


def calcular_estadisticas(dominios):
    """
    Calcula las longitudes, extensiones y nombres principales de los dominios.
    """
    longitudes_nombre = []
    longitudes_extension = []
    extensiones = []
    nombres = []

    for dom in dominios:
        try:
            parte_inicial, extension = dom.rsplit('.', 1)
            nombre = parte_inicial.split('.')[0]  # Parte antes del primer punto
        except ValueError:
            print(f"Dominio mal formado (sin extensión): {dom}")
            continue

        longitudes_nombre.append(len(parte_inicial))
        longitudes_extension.append(len(extension))
        extensiones.append(extension)
        nombres.append(nombre)

    return longitudes_nombre, longitudes_extension, extensiones, nombres


def mostrar_estadisticas(longitudes_nombre, longitudes_extension, extensiones):
    """
    Muestra estadísticas de longitudes y extensiones.
    """
    contador_longitudes = Counter(longitudes_nombre)
    contador_extensiones = Counter(extensiones)

    longitud_media_nombre = sum(longitudes_nombre) / len(longitudes_nombre) if longitudes_nombre else 0.0
    longitud_media_extension = sum(longitudes_extension) / len(longitudes_extension) if longitudes_extension else 0.0

    print(f"\nSe han procesado {len(longitudes_nombre)} dominios.")

    print("\n=== Longitudes de los nombres y su frecuencia ===")
    for length, count in sorted(contador_longitudes.items()):
        print(f"Longitud = {length}: {count} dominios")

    print("\n=== Longitud media del nombre ===")
    print(f"La longitud media (parte antes del punto) es: {longitud_media_nombre:.2f} caracteres.")

    print("\n=== Longitud media de la extensión ===")
    print(f"La longitud media de la extensión es: {longitud_media_extension:.2f} caracteres.")

    print("\n=== Frecuencia de extensiones ===")
    for ext, freq in sorted(contador_extensiones.items(), key=lambda x: x[1], reverse=True):
        print(f".{ext}: {freq}")

    print(f"\nSe han encontrado {len(set(extensiones))} extensiones únicas.")


def mostrar_top_nombres(nombres, top=10):
    """
    Muestra los nombres más habituales (antes del primer punto).
    """
    contador_nombres = Counter(nombres)
    print(f"\n=== Top {top} nombres de dominio más habituales ===")
    for nombre, frecuencia in contador_nombres.most_common(top):
        print(f"{nombre}: {frecuencia} apariciones")

    print(f"\nSe han encontrado {len(set(nombres))} nombres únicos.")


def main():
    ruta_fichero = input("Introduce la ruta del archivo con los dominios: ").strip()
    dominios = leer_dominios_desde_txt(ruta_fichero)
    longitudes_nombre, longitudes_extension, extensiones, nombres = calcular_estadisticas(dominios)
    mostrar_estadisticas(longitudes_nombre, longitudes_extension, extensiones)
    mostrar_top_nombres(nombres, top=10)


if __name__ == "__main__":
    main()
