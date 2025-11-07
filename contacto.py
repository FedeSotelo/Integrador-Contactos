import re
from grupo import  listar_grupos, crear_grupo_interactivo
from archivo import agregar_datosContacto, RUTA_ARCHIVO_CONTACTO, RUTA_ARCHIVO_GRUPO, baja_contacto, modificar_contacto, telefonos_unicos;
import json, os
from functools import reduce

def validar_correo(c: str) -> bool:
    return (c.strip() == "") or bool(re.match(r"[^@]+@[^@]+\.[^@]+", c))

def _telefonos_unicos():
    return telefonos_unicos()

def elegir_grupo():
    """
    Permite al usuario elegir un grupo existente o crear uno nuevo.
    Lee los grupos desde el archivo JSON.
    """
    while True:
        print("\n=== Selección de grupo ===")

        listar_grupos()

        if not os.path.exists(RUTA_ARCHIVO_GRUPO):
            print("No hay archivo de grupos, se creará uno nuevo.")
            return crear_grupo_interactivo()

        try:
            archivo = open(RUTA_ARCHIVO_GRUPO, "r", encoding="UTF-8")
            if os.path.getsize(RUTA_ARCHIVO_GRUPO) == 0:
                grupos = []
            else:
                try:
                    grupos = json.load(archivo)
                except json.JSONDecodeError:
                    print("El archivo de grupos está vacío o dañado. Se reiniciará.")
                    grupos = []
            archivo.close()
        except OSError as error:
            print(f"Error al leer el archivo de grupos: {error}")
            grupos = []

        if not grupos:
            print("No hay grupos activos, se creará uno nuevo.")
            return crear_grupo_interactivo()

        grupos_activos = []
        for g in grupos:
            if not g.get("anulado", False):
                grupos_activos.append(g)

        if len(grupos_activos) == 0:
            print("No hay grupos activos, se creará uno nuevo.")
            return crear_grupo_interactivo()

        print("0: Crear grupo nuevo")
        entrada = input("Ingrese ID de grupo (o 0): ").strip()

        if entrada.isdigit():
            val = int(entrada)
            if val == 0:
                return crear_grupo_interactivo()

            for g in grupos_activos:
                if g["id"] == val:
                    return val

        print("Opción inválida. Intente nuevamente.")


def alta_contacto():
    print("\n=== Alta de contacto ===")

    nombre = input("Nombre: ").strip()
    while nombre == "" or not nombre.replace(" ", "").isalpha():
        print("El nombre es obligatorio y debe contener solo letras.")
        nombre = input("Nombre (obligatorio): ").strip()

    tel1 = input("Teléfono 1: ").strip()
    while tel1 == "" or not tel1.isdigit():
        print("El teléfono debe ser numérico y es obligatorio.")
        tel1 = input("Teléfono 1 (obligatorio): ").strip()

    if tel1 in _telefonos_unicos():
        print(f"El teléfono {tel1} ya existe en otro contacto activo.")
        return

    tel2 = input("Teléfono 2 (opcional): ").strip()
    while tel2 != "" and not tel2.isdigit():
        print("El teléfono debe ser numérico o dejar vacío.")
        tel2 = input("Teléfono 2 (opcional): ").strip()

    correo = input("Correo (opcional): ").strip()
    while not validar_correo(correo):
        print("Correo inválido.")
        correo = input("Correo (opcional): ").strip()

    id_grupo = elegir_grupo()

    contactos = []
    if os.path.exists(RUTA_ARCHIVO_CONTACTO) and os.path.getsize(RUTA_ARCHIVO_CONTACTO) > 0:
        try:
            archivo = open(RUTA_ARCHIVO_CONTACTO, "r", encoding="UTF-8")
            contactos = json.load(archivo)
        except (OSError, json.JSONDecodeError):
            print("Error al leer el archivo de contactos.")
            contactos = []
        finally:
            try:
                archivo.close()
            except Exception as e:
                print("No se pudo cerrar el archivo:", e)

    nuevo_id = 0
    for c in contactos:
        if c["id"] > nuevo_id:
            nuevo_id = c["id"]
    nuevo_id += 1

    nuevo_contacto = {
        "id": nuevo_id,
        "nombre": nombre,
        "tel1": tel1,
        "tel2": tel2,
        "correo": correo,
        "id_grupo": id_grupo,
        "activo": True
    }

    agregar_datosContacto(nuevo_contacto)
    print(f"\nContacto '{nombre}' creado con éxito (ID: {nuevo_id}).")
    "usamos la recursividad para contar contactos activos"
    cantidad = contar_contactos_activos(contactos)
    print("Contactos activos:", cantidad)


    
def resumen_contactos(contactos):
    
    activos = list(filter(lambda c: c.get("activo", True), contactos))

    resumen = list(map(lambda c: f"{c['nombre']} ({c['tel1']})", activos))

    total_tels = reduce(lambda acc, c: acc + (1 if c['tel1'] else 0), activos, 0)

    print("\n=== RESUMEN DE CONTACTOS ===")
    print("Contactos activos:")
    for linea in resumen:
        print(" -", linea)
    print(f"Total de teléfonos registrados: {total_tels}")

def listar_contactos_detallado(filtro_nombre="", filtro_grupo_desc=""):
    """Muestra los contactos activos, con posibilidad de filtrar por nombre o grupo."""

    if not os.path.exists(RUTA_ARCHIVO_CONTACTO) or os.path.getsize(RUTA_ARCHIVO_CONTACTO) == 0:
        print("No hay contactos registrados.")
        return

    try:
        archivo_contactos = open(RUTA_ARCHIVO_CONTACTO, "r", encoding="UTF-8")
        contactos = json.load(archivo_contactos)
        archivo_contactos.close()
    except OSError:
        print("Error al leer el archivo de contactos.")
        return

    grupos = []
    if os.path.exists(RUTA_ARCHIVO_GRUPO) and os.path.getsize(RUTA_ARCHIVO_GRUPO) > 0:
        try:
            archivo_grupos = open(RUTA_ARCHIVO_GRUPO, "r", encoding="UTF-8")
            grupos = json.load(archivo_grupos)
            archivo_grupos.close()
        except OSError:
            grupos = []

    contactos_filtrados = []
    for c in contactos:
        if c.get("activo", True):
            contactos_filtrados.append(c)

    if filtro_nombre.strip() != "":
        temp = []
        for c in contactos_filtrados:
            if filtro_nombre.lower() in c["nombre"].lower():
                temp.append(c)
        contactos_filtrados = temp

    if filtro_grupo_desc.strip() != "":
        temp = []
        for c in contactos_filtrados:
            for g in grupos:
                if not g.get("anulado", False):
                    if g["id"] == c["id_grupo"] and filtro_grupo_desc.lower() in g["nombre"].lower():
                        temp.append(c)
                        break
        contactos_filtrados = temp

    if len(contactos_filtrados) == 0:
        print("No hay contactos que cumplan con los filtros.")
        return

    print("\nID | NOMBRE                | TEL1        | TEL2         | CORREO                         | GRUPO")
    print("---------------------------------------------------------------------------------------------")

    for c in contactos_filtrados:
        grupo_nombre = "(sin grupo)"
        for g in grupos:
            if g["id"] == c["id_grupo"] and not g.get("anulado", False):
                grupo_nombre = g["nombre"]
                break

        print(f"{str(c['id']).ljust(2)} | {c['nombre'].ljust(20)} | {c['tel1'].ljust(12)} | {c['tel2'].ljust(12)} | {c['correo'].ljust(30)} | {grupo_nombre}")
    resumen_contactos(contactos_filtrados)


def eliminar_contacto():
    print("\n=== ELIMINAR CONTACTO ===")
    baja_contacto()

def restaurar_contacto():
    """
    Restaura un contacto dado de baja lógica (activo=False).
    Trabaja con archivo JSON.
    """
    if not os.path.exists(RUTA_ARCHIVO_CONTACTO):
        print("El archivo de contactos no existe.")
        return

    try:
        archivo = open(RUTA_ARCHIVO_CONTACTO, "r", encoding="UTF-8")
        contactos = json.load(archivo)
    except (OSError, json.JSONDecodeError):
        print("Error al leer el archivo de contactos.")
        return
    finally:
        try:
            archivo.close()
        except Exception as e:
            print("No se pudo cerrar el archivo correctamente:", e)

    print("\n=== Contactos inactivos ===")
    hay_inactivos = False
    for c in contactos:
        if not c.get("activo", True):
            print(f"{c['id']} - {c['nombre']} ({c['tel1']})")
            hay_inactivos = True

    if not hay_inactivos:
        print("No hay contactos inactivos para restaurar.")
        return

    codigo_restaurar = input("\nIngrese el ID del contacto a restaurar: ").strip()

    encontrado = False
    for c in contactos:
        if str(c["id"]) == codigo_restaurar and not c.get("activo", True):
            encontrado = True
            print(f"\nContacto encontrado: {c['id']} - {c['nombre']}")
            confirmar = input("¿Desea restaurar este contacto? (s/n): ").strip().lower()

            if confirmar == "s":
                c["activo"] = True
                print("Contacto restaurado correctamente.")
            else:
                print("Operación cancelada.")
            break

    if not encontrado:
        print(f"No se encontró un contacto inactivo con el ID {codigo_restaurar}.")
        return

    try:
        archivo = open(RUTA_ARCHIVO_CONTACTO, "w", encoding="UTF-8")
        json.dump(contactos, archivo, ensure_ascii=False, indent=4)
    except OSError as e:
        print("Error al guardar los cambios:", e)
    finally:
        try:
            archivo.close()
        except Exception as e:
            print("No se pudo cerrar el archivo correctamente:", e)


def editar_contacto():
    print("\n=== MODIFICAR CONTACTO ===")
    modificar_contacto()






    """"
    recursividad"""

def contar_contactos_activos(contactos, i=0):

    if i == len(contactos):
        return 0
    if contactos[i].get("activo", True):
        return 1 + contar_contactos_activos(contactos, i + 1)
    else:
        return contar_contactos_activos(contactos, i + 1)



