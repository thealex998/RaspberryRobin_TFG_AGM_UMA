import csv
import os


def search_coincidence(array1, array2):
    for valor in array1:
        if valor in array2:
            return True
    return False

class Burbuja:
    def __init__(self, dom, ip):
        self.dom = []
        self.dom.append(dom)
        self.ips = []
        self.ips.append(ip)

    def add(self, dominio, ip):
        self.dom.append(dominio)
        self.ips.append(ip)

    def add_ip(self, ip):
        self.ips.append(ip)

    def add_dom(self, dom):
        self.dom.append(dom)

    def search_dom(self, dominio):
        if dominio in self.dom:
            return True
        else:
            return False

    def search_ip(self, ip):
        if ip in self.ips:
            return True
        else:
            return False

class Pecera:
    def __init__(self, cantidad, burbuja):
        self.cantidad: int = cantidad
        self.burbujas = []
        self.burbujas.append(burbuja)

    def add_bubble(self, burbuja):
        self.burbujas.append(burbuja)
        self.cantidad = self.cantidad + 1

    def add_bubble_params(self, dom, ip):
        burbuja_aux = Burbuja(dom, ip)
        self.add_bubble(burbuja_aux)

    def search_ip_pecera(self, ip):
        pos = 0
        for elm in self.burbujas:
            if elm.search_ip(ip):
                return pos
            else:
                pos += 1
        return -1

    def search_dom_pecera(self, dom):
        pos = 0
        for elm in self.burbujas:
            if elm.search_dom(dom):
                return pos
            else:
                pos += 1
        return -1

    def fushion_bubbles_pecera(self, pos1, pos2):
        self.burbujas[pos1].dom = self.burbujas[pos1].dom + self.burbujas[pos2].dom
        self.burbujas[pos1].ips = self.burbujas[pos1].ips + self.burbujas[pos2].ips
        self.burbujas.pop(pos2)
        self.cantidad -= 1

    def add_elemento(self, dom, ip):
        if self.cantidad > 0:
            pos = self.search_ip_pecera(ip)
            if pos == -1:
                pos = self.search_dom_pecera(dom)
                if pos == -1:
                    self.add_bubble_params(dom, ip)
                else:
                    self.burbujas[pos].add_ip(ip)
            else:
                if burbujas.search_dom_pecera(dom) == pos:
                    pass
                else:
                    if burbujas.search_dom_pecera(dom) == -1:
                        self.burbujas[pos].dom.append(dom)
                    else:
                        # fusionamos burbujas
                        burbuja_1_pos = self.search_ip_pecera(ip)
                        burbuja_2_pos = self.search_dom_pecera(dom)
                        self.fushion_bubbles_pecera(burbuja_1_pos, burbuja_2_pos)

                # debemos buscar si está el dominio en la burbuja, si no está metemos el dominio
                # a continuación, debemos buscar todas las burbujas que tienen ese dominio
        else:
            # si accedemos a esta parte del bucle, quiere decir que no hay ninguna burbuja
            self.add_bubble_params(dom, ip)


ruta = "/Volumes/Alejandro SSD/TFG/resultados_ips_unicas_20240228-20240529.csv"
columnas_seleccionadas = [0, 1]
datos = []
# generamos un listado con array doble, que contenga todos los dominios con la IP a la que resuelve
with open(ruta, 'r', encoding='utf-8-sig', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)  # Salta el comentario de rango
    next(reader, None)  # Salta la cabecera real
    datos_temp = [[fila[i] for i in columnas_seleccionadas] for fila in reader]
    datos = datos_temp

# en datos tenemos almacenada toda la información de Dominio-Ip-Ubicación(este último es opcional)
# ahora debemos procesar esa información y ordenarla formando burbujas
unique_list = []
for item in datos:
    if item not in unique_list:
        unique_list.append(item)
datos = unique_list

dominio_inicial, ip_inicial = datos[0]
burbuja_init = Burbuja(dominio_inicial, ip_inicial)
burbujas = Pecera(1, burbuja_init)

burbujas = Pecera(1, burbuja_init)
contador = 1
for elemento in datos:
    contador += 1
    aux_dom = elemento[0]
    aux_ip = elemento[1]
    if aux_ip != "1.1.1.1":
        burbujas.add_elemento(aux_dom, aux_ip) # este elemento es una pecera, la pecera contiene muchas burbujas.
ruta_csv_dominios = "/Volumes/Alejandro SSD/TFG/cluster_doms_20240228-20240529.csv"
ruta_csv_ips = "/Volumes/Alejandro SSD/TFG/cluster_ips_20240228-20240529.csv"
with open(ruta_csv_dominios, 'w', newline='') as archivo_csv_dominios:
    writer_csv_dominios = csv.writer(archivo_csv_dominios)
    writer_csv_dominios.writerow(["Dominio", "Burbuja"])
    i = 1
    for elm in burbujas.burbujas:
        for elm_aux in elm.dom:
            writer_csv_dominios.writerow([elm_aux, i])
        i += 1
with open(ruta_csv_ips, 'w', newline='') as archivo_csv_ips:
    writer_csv_ips = csv.writer(archivo_csv_ips)
    writer_csv_ips.writerow(["IP", "Burbuja"])
    i = 1
    for elm in burbujas.burbujas:
        for elm_aux in elm.ips:
            writer_csv_ips\
                .writerow([elm_aux, i])
        i += 1

print("Número de datos procesados: ")
print(contador)
print("Número de burbujas diferentes: ")
print(burbujas.cantidad)
