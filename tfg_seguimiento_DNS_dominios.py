import csv
import socket
from datetime import datetime

# Abre el flujo hacia la ruta en la que están almacenados los dominios
f = open("dominios.txt")
reader = csv.reader(f)

# Permite guardar el momento en el que se realiza la primera petición en formato UTC
now = datetime.utcnow()
ruta_guardado = "/Path_Salida/"
ruta_guardado = ruta_guardado + f'res_csv_iP{now}.csv'
robin_salida = open(ruta_guardado, 'w', newline='')
writer = csv.writer(robin_salida)

# Bucle para obtener la dirección IP asociada a cada dominio y guardar los resultados en un fichero
for line in reader:
    try:
        dir_IP = socket.gethostbyname(line[0])
        writer.writerow([line[0], dir_IP])
    except:
        dir_IP = 0
        writer.writerow([line[0], dir_IP])
f.close
robin_salida.close
