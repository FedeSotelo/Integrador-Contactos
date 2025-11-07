from interacciones import contar_interacciones_activas
from archivo import RUTA_ARCHIVO_CONTACTO, RUTA_ARCHIVO_GRUPO, RUTA_ARCHIVO_INTERACCIONES,leer_interacciones
import json, os

def cantidad_contactos_por_grupo():
    print("\n=== Cantidad de contactos por grupo ===")

    if not os.path.exists(RUTA_ARCHIVO_GRUPO) or not os.path.exists(RUTA_ARCHIVO_CONTACTO):
        print("No hay datos disponibles.")
        return
    with open(RUTA_ARCHIVO_GRUPO, "r", encoding="UTF-8") as gfile:
        grupos = json.load(gfile)

    with open(RUTA_ARCHIVO_CONTACTO, "r", encoding="UTF-8") as cfile:
        contactos = json.load(cfile)

    grupos_activos = [g for g in grupos if not g.get("anulado", False)]

    if not grupos_activos:
        print("(no hay grupos activos para mostrar)")
        return

    for g in grupos_activos:
        gid = g["id"]
        nombre = g["nombre"]
        cantidad = len([
            c for c in contactos
            if c.get("id_grupo") == gid and c.get("activo", True)
        ])
        print(f"- {nombre}: {cantidad} contacto(s)")



def promedio_interacciones_por_contacto():
    print("\n=== Promedio de interacciones por contacto ===")

    if not os.path.exists(RUTA_ARCHIVO_CONTACTO) or not os.path.exists(RUTA_ARCHIVO_INTERACCIONES):
        print("No hay datos suficientes para calcular el promedio.")
        return

    with open(RUTA_ARCHIVO_CONTACTO, "r", encoding="UTF-8") as arch_contactos:
        contactos = json.load(arch_contactos)

    with open(RUTA_ARCHIVO_INTERACCIONES, "r", encoding="UTF-8") as arch_inter:
        interacciones = json.load(arch_inter)

    contactos_activos = [c for c in contactos if c.get("activo", True)]

    interacciones_activas = [i for i in interacciones if not i.get("anulado", False)]

    total_contactos = len(contactos_activos)
    total_interacciones = len(interacciones_activas)

    promedio = total_interacciones / total_contactos if total_contactos > 0 else 0
    print(f"Promedio de interacciones por contacto: {promedio:.2f}")




def porcentaje_contactos_activos():

    print("\n=== Porcentaje de contactos activos ===")

    if not os.path.exists(RUTA_ARCHIVO_CONTACTO) or not os.path.exists(RUTA_ARCHIVO_INTERACCIONES):
        print("No hay datos suficientes para calcular el porcentaje.")
        return

    with open(RUTA_ARCHIVO_CONTACTO, "r", encoding="UTF-8") as cfile:
        contactos = json.load(cfile)

    with open(RUTA_ARCHIVO_INTERACCIONES, "r", encoding="UTF-8") as ifile:
        interacciones = json.load(ifile)

    contactos_activos = [c for c in contactos if c.get("activo", True)]
    total = len(contactos_activos)

    if total == 0:
        print("No hay contactos activos registrados.")
        return

    activos_con_interaccion = [
        c for c in contactos_activos
        if any(
            i.get("id_contacto") == c.get("id") and not i.get("anulado", False)
            for i in interacciones
        )
    ]

    porcentaje = (len(activos_con_interaccion) / total) * 100
    print(f"Porcentaje de contactos con al menos una interacción activa: {porcentaje:.2f}%")


def contacto_con_mas_y_menos_interacciones():

    print("\n=== Contactos con más y menos interacciones ===")

    if not os.path.exists(RUTA_ARCHIVO_CONTACTO) or not os.path.exists(RUTA_ARCHIVO_INTERACCIONES):
        print("No hay contactos o interacciones registradas.")
        return

    with open(RUTA_ARCHIVO_CONTACTO, "r", encoding="UTF-8") as cfile:
        contactos = json.load(cfile)

    with open(RUTA_ARCHIVO_INTERACCIONES, "r", encoding="UTF-8") as ifile:
        interacciones = json.load(ifile)

    contactos_activos = [c for c in contactos if c.get("activo", True)]
    interacciones_activas = [i for i in interacciones if not i.get("anulado", False)]

    if not contactos_activos or not interacciones_activas:
        print("No hay contactos o interacciones activas registradas.")
        return

    conteo = {c["id"]: 0 for c in contactos_activos}
    for i in interacciones_activas:
        id_contacto = i.get("id_contacto")
        if id_contacto in conteo:
            conteo[id_contacto] += 1

    if not conteo:
        print("No hay datos suficientes para mostrar estadísticas.")
        return

    max_id = max(conteo, key=conteo.get)
    min_id = min(conteo, key=conteo.get)

    contacto_max = next((c for c in contactos_activos if c["id"] == max_id), None)
    contacto_min = next((c for c in contactos_activos if c["id"] == min_id), None)

    print("\nContacto con mas interacciones:")
    print(f"- {contacto_max['nombre']} ({conteo[max_id]} interacciones)")

    print("\nContacto con menos interacciones:")
    print(f"- {contacto_min['nombre']} ({conteo[min_id]} interacciones)")



def matriz_contactos_por_grupo_y_tipo():
 
    print("\n=== Matriz de interacciones por grupo y tipo ===")

    if not all(os.path.exists(p) for p in [RUTA_ARCHIVO_GRUPO, RUTA_ARCHIVO_CONTACTO, RUTA_ARCHIVO_INTERACCIONES]):
        print("No hay datos suficientes para generar la matriz.")
        return

    with open(RUTA_ARCHIVO_GRUPO, "r", encoding="UTF-8") as gfile:
        grupos = json.load(gfile)
    with open(RUTA_ARCHIVO_CONTACTO, "r", encoding="UTF-8") as cfile:
        contactos = json.load(cfile)
    with open(RUTA_ARCHIVO_INTERACCIONES, "r", encoding="UTF-8") as ifile:
        interacciones = json.load(ifile)

    grupos_activos = [g for g in grupos if not g.get("anulado", False)]
    contactos_activos = [c for c in contactos if c.get("activo", True)]
    interacciones_activas = [i for i in interacciones if not i.get("anulado", False)]

    if not grupos_activos or not interacciones_activas:
        print("No hay datos activos suficientes para generar la matriz.")
        return

    tipos_encontrados = []
    for i in interacciones_activas:
        tipo = i["tipo"]
        if tipo not in tipos_encontrados:
            tipos_encontrados.append(tipo)


    columnas = tipos_encontrados
    matriz = []

    for g in grupos_activos:
        fila = [g["nombre"]]
        for tipo in columnas:
            cant = sum(
                1 for i in interacciones_activas
                if i["tipo"] == tipo and any(
                    c["id"] == i["id_contacto"] and c["id_grupo"] == g["id"] and c["activo"]
                    for c in contactos_activos
                )
            )
            fila.append(cant)
        matriz.append(fila)

    print("\nInteracciones por grupo y tipo:")
    print("GRUPO".ljust(15) + " | " + " | ".join(c.ljust(12) for c in columnas))
    print("-" * (17 + len(columnas) * 15))


    for fila in matriz[:10]:
        print(fila[0].ljust(15) + " | " + " | ".join(str(x).ljust(12) for x in fila[1:]))


        
def cantidad_interacciones_activas():
    interacciones = leer_interacciones(incluir_anuladas=True)
    total = contar_interacciones_activas(interacciones)
    print(f"Total de interacciones activas: {total}")