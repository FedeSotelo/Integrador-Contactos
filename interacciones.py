import json
import os
from archivo import obtener_nombre_y_tel,  elegir_tipo_interaccion, agregar_datosInteraccion,  RUTA_ARCHIVO_INTERACCIONES, RUTA_ARCHIVO_CONTACTO, RUTA_ARCHIVO_GRUPO,next_id_interaccion, leer_interacciones,modificar_interaccion, eliminar_interaccion, restaurar_interaccion,listar_tipos, alta_tipo, baja_tipo, modificar_tipo
from functools import reduce


def next_id(d: dict) -> int:
    if not d:
        return 1
    return reduce(lambda a, b: a if a > b else b, d.keys()) + 1


from archivo import RUTA_ARCHIVO_CONTACTO

def elegir_contacto():
    """
    Muestra los contactos activos desde contacto.json y permite seleccionar uno por ID.
    Devuelve el ID del contacto elegido si existe, o None si no es válido.
    """
    if not os.path.exists(RUTA_ARCHIVO_CONTACTO) or os.path.getsize(RUTA_ARCHIVO_CONTACTO) == 0:
        print("No hay contactos activos para seleccionar.")
        return None

    try:
        with open(RUTA_ARCHIVO_CONTACTO, "r", encoding="UTF-8") as archivo:
            contactos = json.load(archivo)
    except (OSError, json.JSONDecodeError) as error:
        print(f"No se pudo leer el archivo de contactos: {error}")
        return None

    contactos_activos = [c for c in contactos if c.get("activo", True)]

    if not contactos_activos:
        print("No hay contactos activos para seleccionar.")
        return None

    print("\n=== LISTADO DE CONTACTOS ACTIVOS ===")
    print(f'{"ID":<5}{"NOMBRE":<20}{"TEL1":<15}{"TEL2":<15}{"CORREO":<25}{"GRUPO":<10}')
    print("-" * 90)

    for c in contactos_activos:
        print(f"{c['id']:<5}{c['nombre']:<20}{c['tel1']:<15}{c['tel2']:<15}{c['correo']:<25}{c['id_grupo']:<10}")

    entrada = input("\nIngrese el ID del contacto: ").strip()
    if any(str(c['id']) == entrada for c in contactos_activos):
        return entrada
    else:
        print("ID inválido o contacto no activo.")
        return None



def crear_interaccion():
    print("\n=== CREAR NUEVA INTERACCIÓN ===")

    id_contacto = elegir_contacto()
    if id_contacto is None:
        print("Operación cancelada.")
        return

    tipo = elegir_tipo_interaccion()
    if tipo is None:
        print("Operación cancelada.")
        return

    descripcion = input("Descripción: ").strip()
    while descripcion == "":
        print("La descripción no puede estar vacía.")
        descripcion = input("Descripción: ").strip()

    fecha = input("Fecha (DD/MM/AAAA): ").strip()
    while not _validar_fecha_completa(fecha):
        print("Formato inválido. Usa DD/MM/AAAA o DD-MM-AAAA.")
        fecha = input("Fecha (DD/MM/AAAA): ").strip()

    nuevo_id = next_id_interaccion()

    nueva_interaccion = {
        "id": nuevo_id,
        "id_contacto": id_contacto,
        "descripcion": descripcion,
        "fecha": fecha,
        "tipo": tipo,
        "anulado": False
    }

    agregar_datosInteraccion(nueva_interaccion)


def listar_interacciones(incluir_anuladas=False):
    filas = leer_interacciones(incluir_anuladas)
    if not filas:
        print("(no hay interacciones)")
        return []

    print("\n=== LISTA DE INTERACCIONES ===")
    print(f'{"ID":<5}{"CONTACTO":<20}{"DESCRIPCIÓN":<25}{"FECHA":<12}{"TIPO":<15}')
    print("-----------------------------------------------------------------------")

    for fila in filas:
        resultado = obtener_nombre_y_tel(fila["id_contacto"], RUTA_ARCHIVO_CONTACTO)

        if resultado is None:
            nombre = "(desconocido)"
        else:
            nombre, _ = resultado

        print(f"{fila['id']:<5}{nombre:<20}{fila['descripcion']:<25}{fila['fecha']:<12}{fila['tipo']:<15}")

    return filas


def editar_interaccion():
    listar_interacciones()
    modificar_interaccion()




def baja_interaccion():
    listar_interacciones()
    eliminar_interaccion()


def reactivar_interaccion():
    listar_interacciones(incluir_anuladas=True)
    restaurar_interaccion()

def ver_historial_por_contacto():
    cid = input("Ingrese el ID del contacto: ").strip()
    if not cid.isdigit():
        print("ID inválido.")
        return

    # Obtener nombre y teléfono desde el JSON
    nombre, telefono = obtener_nombre_y_tel(cid, RUTA_ARCHIVO_CONTACTO)
    if nombre == "(desconocido)":
        print("No existe un contacto activo con ese ID.")
        return

    # Verificar existencia del archivo de interacciones
    if not os.path.exists(RUTA_ARCHIVO_INTERACCIONES):
        print("No hay interacciones registradas.")
        return

    print(f"\nHistorial de interacciones de {nombre} (tel: {telefono}):")
    encontrado = False

    try:
        with open(RUTA_ARCHIVO_INTERACCIONES, "rt", encoding="UTF-8") as file:
            for linea in file:
                datos = linea.strip().split(";")
                if len(datos) >= 6:
                    id_interaccion = datos[0].strip()
                    id_contacto = datos[1].strip()
                    descripcion = datos[2].strip()
                    fecha = datos[3].strip()
                    tipo = datos[4].strip()
                    anulado = datos[5].strip().lower()

                    # Mostrar solo si está activo (false o vacío)
                    if id_contacto == cid and (anulado == "false" or anulado == ""):
                        print(f"- {fecha}: {descripcion} ({tipo})")
                        encontrado = True

        if not encontrado:
            print("Ese contacto no tiene interacciones activas.")
    except OSError as error:
        print(f"Error al leer el archivo de interacciones: {error}")




def ver_historial_por_grupo():
    print("\n=== HISTORIAL POR GRUPO ===")

    # Verificar existencia de archivos
    if not all(os.path.exists(p) for p in [RUTA_ARCHIVO_GRUPO, RUTA_ARCHIVO_CONTACTO, RUTA_ARCHIVO_INTERACCIONES]):
        print("Faltan archivos necesarios (grupo, contacto o interacciones).")
        return

    # Leer grupos y contactos desde JSON
    try:
        with open(RUTA_ARCHIVO_GRUPO, "r", encoding="UTF-8") as gfile:
            grupos = json.load(gfile)
        with open(RUTA_ARCHIVO_CONTACTO, "r", encoding="UTF-8") as cfile:
            contactos = json.load(cfile)
    except (OSError, json.JSONDecodeError):
        print("Error al leer archivos JSON.")
        return

    # Filtrar grupos activos
    grupos_activos = [g for g in grupos if not g.get("anulado", False)]
    if not grupos_activos:
        print("No hay grupos activos.")
        return

    print("\n=== LISTA DE GRUPOS ===")
    print(f'{"ID":<5}{"NOMBRE":<20}')
    print("-" * 25)
    for g in grupos_activos:
        print(f"{g['id']:<5}{g['nombre']:<20}")

    gid = input("\nIngrese el ID del grupo: ").strip()
    if not gid.isdigit():
        print("ID de grupo inválido.")
        return

    grupo = next((g for g in grupos_activos if str(g["id"]) == gid), None)
    if not grupo:
        print("No se encontró ese grupo o está anulado.")
        return

    # Buscar contactos activos en ese grupo
    contactos_en_grupo = [
        c for c in contactos
        if c.get("activo", True) and str(c.get("id_grupo")) == gid
    ]
    if not contactos_en_grupo:
        print("Este grupo no tiene contactos activos.")
        return

    ids_contactos = [str(c["id"]) for c in contactos_en_grupo]

    # Leer interacciones desde archivo TXT
    print(f"\nHistorial de interacciones del grupo '{grupo['nombre']}':")
    try:
        with open(RUTA_ARCHIVO_INTERACCIONES, "rt", encoding="UTF-8") as file:
            lineas = file.readlines()

        encontrado = False
        for linea in lineas:
            datos = linea.strip().split(";")
            if len(datos) >= 6:
                id_interaccion = datos[0]
                id_contacto = datos[1]
                descripcion = datos[2]
                fecha = datos[3]
                tipo = datos[4]
                anulado = datos[5].strip().lower()

                if id_contacto in ids_contactos and anulado != "true":
                    contacto = next((c for c in contactos_en_grupo if str(c["id"]) == id_contacto), None)
                    nombre = contacto["nombre"] if contacto else "(desconocido)"
                    print(f"- {nombre} ({fecha}): {descripcion} ({tipo})")
                    encontrado = True

        if not encontrado:
            print("Este grupo no tiene interacciones activas.")
    except OSError as e:
        print(f"Error al acceder al archivo de interacciones: {e}")


def _es_bisiesto(anio: int) -> bool:
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

def _dias_en_mes(mes: int, anio: int) -> int:
    if mes in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif mes in [4, 6, 9, 11]:
        return 30
    elif mes == 2:
        return 29 if _es_bisiesto(anio) else 28
    else:
        return 0   # mes invalido
    
def _validar_fecha_completa(fecha: str) -> bool:
    if "/" in fecha:
        partes = fecha.split("/")
    elif "-" in fecha:
        partes = fecha.split("-")
    else:
        return False

    if len(partes) != 3:
        return False

    dia, mes, anio = partes
    if not (dia.isdigit() and mes.isdigit() and anio.isdigit()):
        return False

    dia, mes, anio = int(dia), int(mes), int(anio)

    if not (1 <= mes <= 12):
        return False

    max_dias = _dias_en_mes(mes, anio)
    if not (1 <= dia <= max_dias):
        return False

    return True



def contar_interacciones_activas(interacciones, i=0):
    '''
        ESTO CUENTA cuantas interacciones activas hay de forma recursiva.
         recibe una lista de interacciones.
         devuelve la cantidad de interacciones activas (activo=True).
    '''
    if i == len(interacciones):
        return 0
    if interacciones[i].get("activo", "true").lower() == "true":
        return 1 + contar_interacciones_activas(interacciones, i + 1)
    else:
        return contar_interacciones_activas(interacciones, i + 1)


       