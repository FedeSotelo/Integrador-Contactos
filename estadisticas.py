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

    try:
        with open(RUTA_ARCHIVO_INTERACCIONES, "r", encoding="UTF-8") as arch_inter:
            lineas = arch_inter.readlines()
    except OSError as error:
        print(f"No se pudo abrir el archivo de interacciones: {error}")
        return

    interacciones = []
    for linea in lineas:
        datos = linea.strip().split(";")
        if len(datos) >= 6 and datos[5].lower() != "true":  
            interacciones.append(datos)

    if not interacciones:
        print("No hay interacciones activas.")
        return

    ids_contactos = [i[1] for i in interacciones]
    total_contactos = len(set(ids_contactos))
    promedio = len(interacciones) / total_contactos if total_contactos > 0 else 0

    print(f"Promedio de interacciones por contacto: {promedio:.2f}")

def porcentaje_contactos_activos():
    print("\n=== Porcentaje de contactos activos ===")

    if not os.path.exists(RUTA_ARCHIVO_CONTACTO) or not os.path.exists(RUTA_ARCHIVO_INTERACCIONES):
        print("No hay datos suficientes para calcular el porcentaje.")
        return

    try:
        with open(RUTA_ARCHIVO_CONTACTO, "r", encoding="UTF-8") as cfile:
            contactos = json.load(cfile)
    except (OSError, json.JSONDecodeError):
        print("Error al leer el archivo de contactos.")
        return

    interacciones = []
    try:
        with open(RUTA_ARCHIVO_INTERACCIONES, "r", encoding="UTF-8") as ifile:
            for linea in ifile:
                datos = linea.strip().split(";")
                if len(datos) >= 6 and datos[5].lower() != "true":
                    interacciones.append({
                        "id": datos[0],
                        "id_contacto": datos[1],
                        "tipo": datos[4]
                    })
    except OSError as error:
        print(f"No se pudo leer el archivo de interacciones: {error}")
        return

    contactos_activos = [c for c in contactos if c.get("activo", True)]
    total = len(contactos_activos)

    if total == 0:
        print("No hay contactos activos registrados.")
        return

    activos_con_interaccion = []
    for c in contactos_activos:
        for i in interacciones:
            if i["id_contacto"] == str(c["id"]):
                activos_con_interaccion.append(c)
                break 

    porcentaje = (len(activos_con_interaccion) / total) * 100
    print(f"Porcentaje de contactos con al menos una interacción activa: {porcentaje:.2f}%")

def contacto_con_mas_y_menos_interacciones():
    print("\n=== Contactos con más y menos interacciones ===")

    if not os.path.exists(RUTA_ARCHIVO_CONTACTO) or not os.path.exists(RUTA_ARCHIVO_INTERACCIONES):
        print("No hay contactos o interacciones registradas.")
        return

    try:
        with open(RUTA_ARCHIVO_CONTACTO, "r", encoding="UTF-8") as cfile:
            contactos = json.load(cfile)
    except (OSError, json.JSONDecodeError):
        print("Error al leer el archivo de contactos.")
        return

    interacciones = []
    try:
        with open(RUTA_ARCHIVO_INTERACCIONES, "r", encoding="UTF-8") as ifile:
            for linea in ifile:
                datos = linea.strip().split(";")
                if len(datos) >= 6 and datos[5].lower() != "true":
                    interacciones.append({
                        "id": datos[0],
                        "id_contacto": datos[1],
                        "tipo": datos[4]
                    })
    except OSError as error:
        print(f"No se pudo leer el archivo de interacciones: {error}")
        return

    contactos_activos = [c for c in contactos if c.get("activo", True)]
    if not contactos_activos or not interacciones:
        print("No hay contactos o interacciones activas registradas.")
        return

    conteo = {str(c["id"]): 0 for c in contactos_activos}
    for i in interacciones:
        id_contacto = str(i["id_contacto"])
        if id_contacto in conteo:
            conteo[id_contacto] += 1

    if not conteo:
        print("No hay datos suficientes para mostrar estadísticas.")
        return

    max_id = max(conteo, key=conteo.get)
    min_id = min(conteo, key=conteo.get)

    contacto_max = next((c for c in contactos_activos if str(c["id"]) == max_id), None)
    contacto_min = next((c for c in contactos_activos if str(c["id"]) == min_id), None)

    print("\nContacto con más interacciones:")
    if contacto_max:
        print(f"- {contacto_max['nombre']} ({conteo[max_id]} interacciones)")
    else:
        print("- (no encontrado)")

    print("\nContacto con menos interacciones:")
    if contacto_min:
        print(f"- {contacto_min['nombre']} ({conteo[min_id]} interacciones)")
    else:
        print("- (no encontrado)")



def matriz_contactos_por_grupo_y_tipo():
    print("\n=== Matriz de interacciones por grupo y tipo ===")

    if not all(os.path.exists(p) for p in [RUTA_ARCHIVO_GRUPO, RUTA_ARCHIVO_CONTACTO, RUTA_ARCHIVO_INTERACCIONES]):
        print("No hay datos suficientes para generar la matriz.")
        return

    with open(RUTA_ARCHIVO_GRUPO, "r", encoding="UTF-8") as gfile:
        grupos = json.load(gfile)
    with open(RUTA_ARCHIVO_CONTACTO, "r", encoding="UTF-8") as cfile:
        contactos = json.load(cfile)

    interacciones = []
    with open(RUTA_ARCHIVO_INTERACCIONES, "r", encoding="UTF-8") as ifile:
        for linea in ifile:
            datos = linea.strip().split(";")
            if len(datos) >= 6 and datos[5].lower() != "true":
                interacciones.append({
                    "id": datos[0],
                    "id_contacto": datos[1],
                    "tipo": datos[4]
                })

    grupos_activos = [g for g in grupos if not g.get("anulado", False)]
    contactos_activos = [c for c in contactos if c.get("activo", True)]

    if not grupos_activos or not interacciones:
        print("No hay datos activos suficientes para generar la matriz.")
        return

    tipos_encontrados = []
    for i in interacciones:
        if i["tipo"] not in tipos_encontrados:
            tipos_encontrados.append(i["tipo"])

    columnas = tipos_encontrados
    matriz = []

    for g in grupos_activos:
        fila = [g["nombre"]]
        for tipo in columnas:
            cant = 0
            for i in interacciones:
                if i["tipo"] == tipo:
                    for c in contactos_activos:
                        if str(c["id"]) == str(i["id_contacto"]) and str(c["id_grupo"]) == str(g["id"]):
                            cant += 1
                            break
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