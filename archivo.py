RUTA_ARCHIVO_CONTACTO = r"F:\Feden\Desktop\Materias UADE\2DO CUATRIMESTRE\PROGRAMACION 1\contacto.json"
RUTA_ARCHIVO_GRUPO = r"F:\Feden\Desktop\Materias UADE\2DO CUATRIMESTRE\PROGRAMACION 1\grupo.json"
RUTA_ARCHIVO_TIPOS = r"F:\Feden\Desktop\Materias UADE\2DO CUATRIMESTRE\PROGRAMACION 1\tipos_interaccion.txt"
RUTA_ARCHIVO_INTERACCIONES = r"F:\Feden\Desktop\Materias UADE\2DO CUATRIMESTRE\PROGRAMACION 1\interacciones.txt"


import json
import os;

""""
grupos
"""
def agregar_datosGrupo(nuevo_Grupo):
    try:
        if os.path.exists(RUTA_ARCHIVO_GRUPO):
            if os.path.getsize(RUTA_ARCHIVO_GRUPO) > 0:
                with open(RUTA_ARCHIVO_GRUPO, 'r', encoding="UTF-8") as datos:
                    grupos = json.load(datos)
            else:
                grupos = []
        else:
            grupos = []

        grupos.append(nuevo_Grupo)

        with open(RUTA_ARCHIVO_GRUPO, 'w', encoding="UTF-8") as datos:
            json.dump(grupos, datos, ensure_ascii=False)

        print(f'Se ha agregado el grupo {nuevo_Grupo["nombre"]} correctamente.')

    except (FileNotFoundError, OSError) as error:
        print(f'Error: {error}')

def listar_grupos():
    """
    Lista todos los grupos guardados en el archivo JSON, mostrando solo los activos.
    """
    print("\n=== LISTA DE GRUPOS ===")
    print(f'{"ID":<5}{"NOMBRE":<25}')
    print("-" * 30)

    if not os.path.exists(RUTA_ARCHIVO_GRUPO) or os.path.getsize(RUTA_ARCHIVO_GRUPO) == 0:
        print("(no hay grupos a mostrar)")
        return

    try:
        with open(RUTA_ARCHIVO_GRUPO, "r", encoding="UTF-8") as arch:
            grupos = json.load(arch)
    except (OSError, json.JSONDecodeError):
        print("Error al leer el archivo de grupos.")
        return

    grupos_activos = [g for g in grupos if not g.get("anulado", False)]

    if not grupos_activos:
        print("(no hay grupos activos)")
        return

    for g in grupos_activos:
        print(f"{str(g['id']):<5}{g['nombre']:<25}")

def listar_grupos_inactivos():
    """
    Muestra los grupos inactivos (anulados) guardados en el archivo.
    """
    try:
        arch = open(RUTA_ARCHIVO_GRUPO, "rt", encoding="UTF-8")
    except OSError as error:
        print(f"No se pudo leer el archivo de grupos: {error}")
    else:
        print("\n=== LISTA DE GRUPOS INACTIVOS ===")
        print(f'{"ID":<5}{"NOMBRE":<25}{"ACTIVO":<10}')
        print("-" * 40)
        linea = arch.readline()
        if linea == "":
            print("(no hay grupos a mostrar)")
        while linea != "":
            datos = linea.strip().split(";")
            # Si manejás un campo "activo" o "anulado" en la tercera posición
            if len(datos) >= 3:
                activo = datos[2].strip().lower()
                if activo == "false" or activo == "0":
                    print(f"{datos[0]:<5}{datos[1]:<25}{activo:<10}")
            linea = arch.readline()
        arch.close()


def eliminar_grupo():
   
    try:
        archivo = open(RUTA_ARCHIVO_GRUPO, "r", encoding="UTF-8")
        grupos = json.load(archivo)
        archivo.close()
    except (OSError, json.JSONDecodeError):
        print("Error al leer el archivo de grupos.")
        return

    codigo_baja = input("Ingrese el ID del grupo a eliminar: ").strip()
    encontrado = False

    for g in grupos:
        if str(g["id"]) == codigo_baja:
            encontrado = True
            print(f"\nGrupo encontrado: {g['id']} - {g['nombre']}")
            eleccion = input("¿Eliminar definitivamente (F) o marcar como inactivo (L)? [F/L]: ").strip().lower()

            if eleccion == "f":
                grupos.remove(g)
                print(f"Grupo {g['nombre']} eliminado definitivamente.")
            else:
                g["anulado"] = True
                print(f"Grupo '{g['nombre']}' marcado como inactivo (baja lógica).")
            break

    if not encontrado:
        print(f"No se encontró el grupo {codigo_baja}.")
        return

    try:
        archivo = open(RUTA_ARCHIVO_GRUPO, "w", encoding="UTF-8")
        json.dump(grupos, archivo, ensure_ascii=False, indent=4)
        archivo.close()
    except OSError as e:
        print("Error al escribir el archivo:", e)

def restaurar_grupo():
  
    codigo_restaurar = input("Ingrese el ID del grupo a restaurar: ").strip()
    encontrado = False

    try:
        archivo = open(RUTA_ARCHIVO_GRUPO, "r", encoding="UTF-8")
        grupos = json.load(archivo)
        archivo.close()
    except (OSError, json.JSONDecodeError):
        print("Error al leer el archivo de grupos.")
        return

    for g in grupos:
        if str(g["id"]) == codigo_restaurar and g.get("anulado", False):
            encontrado = True
            print(f"\nGrupo encontrado: {g['id']} - {g['nombre']}")
            confirmar = input("¿Desea restaurar este grupo? (s/n): ").strip().lower()

            if confirmar == "s":
                g["anulado"] = False
                print(f"Grupo '{g['nombre']}' restaurado correctamente.")
            else:
                print("Operación cancelada.")
            break

    if not encontrado:
        print(f"No se encontró un grupo inactivo con el ID {codigo_restaurar}.")
        return

    try:
        archivo = open(RUTA_ARCHIVO_GRUPO, "w", encoding="UTF-8")
        json.dump(grupos, archivo, ensure_ascii=False, indent=4)
        archivo.close()
    except OSError as error:
        print("Error al escribir el archivo:", error)


def editar_grupo():

    listar_grupos()
    codigo_modif = input("Ingrese el ID del grupo a modificar: ").strip()
    encontrado = False

    try:
        archivo = open(RUTA_ARCHIVO_GRUPO, "r", encoding="UTF-8")
        grupos = json.load(archivo)
        archivo.close()
    except (OSError, json.JSONDecodeError):
        print("Error al leer el archivo de grupos.")
        return

    for g in grupos:
        if str(g["id"]) == codigo_modif and not g.get("anulado", False):
            encontrado = True
            print(f"\nGrupo encontrado: {g['id']} - {g['nombre']}")
            nuevo_nombre = input(f"Nuevo nombre ({g['nombre']}): ").strip()

            if nuevo_nombre == "":
                nuevo_nombre = g["nombre"]
            else:
                while not nuevo_nombre.replace(" ", "").isalpha():
                    print("El nombre solo puede tener letras y espacios.")
                    nuevo_nombre = input(f"Nuevo nombre ({g['nombre']}): ").strip()
                    if nuevo_nombre == "":
                        nuevo_nombre = g["nombre"]
                        break

                # Evitar duplicados
                for otro in grupos:
                    if otro != g and otro["nombre"].lower() == nuevo_nombre.lower() and not otro.get("anulado", False):
                        print("Ya existe otro grupo activo con ese nombre.")
                        return

            g["nombre"] = nuevo_nombre
            print(f"Grupo {g['id']} modificado correctamente.")
            break

    if not encontrado:
        print(f"No se encontró un grupo activo con el ID {codigo_modif}.")
        return

    try:
        archivo = open(RUTA_ARCHIVO_GRUPO, "w", encoding="UTF-8")
        json.dump(grupos, archivo, ensure_ascii=False, indent=4)
        archivo.close()
    except OSError as error:
        print("Error al escribir el archivo:", error)

def buscar_grupo_por_id(gid):
 
    if not os.path.exists(RUTA_ARCHIVO_GRUPO) or os.path.getsize(RUTA_ARCHIVO_GRUPO) == 0:
        return None

    try:
        archivo = open(RUTA_ARCHIVO_GRUPO, "r", encoding="UTF-8")
        grupos = json.load(archivo)
        archivo.close()
    except (OSError, json.JSONDecodeError):
        print("Error al leer el archivo de grupos.")
        return None

    for g in grupos:
        if g["id"] == gid:
            return (g["id"], g["nombre"], not g["anulado"])
    
    return None


def listar_grupos_inactivos():
   
    print("\n=== Grupos inactivos ===")
    if not os.path.exists(RUTA_ARCHIVO_GRUPO) or os.path.getsize(RUTA_ARCHIVO_GRUPO) == 0:
        print("(no hay grupos inactivos)")
        return

    try:
        archivo = open(RUTA_ARCHIVO_GRUPO, "r", encoding="UTF-8")
        grupos = json.load(archivo)
        archivo.close()
    except OSError as error:
        print(f"Error al leer el archivo: {error}")
        return

    hay_inactivos = False
    for g in grupos:
        if g.get("anulado", False):
            print(f"{str(g['id']).ljust(3)} - {g['nombre'].strip().ljust(20)}")
            hay_inactivos = True

    if not hay_inactivos:
        print("(no hay grupos inactivos)")

"""
contactos
"""
def agregar_datosContacto(nuevo_contacto):
    try:
        if os.path.exists(RUTA_ARCHIVO_CONTACTO):
            if os.path.getsize(RUTA_ARCHIVO_CONTACTO) > 0:
                datos = open(RUTA_ARCHIVO_CONTACTO, 'r', encoding="UTF-8")
                contactos = json.load(datos)
                datos.close()
            else:
                contactos = []
        else:
            contactos = []

        contactos.append(nuevo_contacto)

        datos = open(RUTA_ARCHIVO_CONTACTO, 'w', encoding="UTF-8")
        json.dump(contactos, datos, ensure_ascii=False)
        datos.close()

        print(f"Se ha agregado el contacto {nuevo_contacto['nombre']} correctamente.")

    except OSError as error:
        print(f"Error al acceder al archivo: {error}")

    "USAMOS RECURSIVIDAD PARA BUSCAR CONTACTO POR ID ESTA FUNCION SE LLAMA EN OBTENER NOMBRE Y TEL"

def buscar_contacto_por_id(contactos, id_buscar, i=0):
    if i == len(contactos):
        return None
    if contactos[i]["id"] == id_buscar:
        return contactos[i]
    return buscar_contacto_por_id(contactos, id_buscar, i + 1)


def obtener_nombre_y_tel(id_contacto, archivo):
    try:
        with open(archivo, "r", encoding="UTF-8") as arch:
            contactos = json.load(arch)
    except (OSError, json.JSONDecodeError):
        print(f"No se pudo abrir el archivo {archivo}")
        return None

    for c in contactos:
        if str(c["id"]) == str(id_contacto) and c.get("activo", True):
            return (c["nombre"], c["tel1"])

    return ("(desconocido)", "")




def leer_contactos(archivo):
    try:
        arch = open(archivo, "rt", encoding="UTF-8")
    except OSError as error:
        print(f"No se pudo leer el archivo {archivo}: {error}")
    else:
        print("\n=== LISTADO DE CONTACTOS ===")
        print(f'{"ID":<5}{"NOMBRE":<20}{"TEL1":<15}{"TEL2":<15}{"CORREO":<25}{"GRUPO":<10}{"ACTIVO":<10}')
        linea = arch.readline()
        while linea != "":
            datos = linea.strip().split(";")
            if len(datos) >= 7:
                idc = datos[0]
                nombre = datos[1]
                tel1 = datos[2]
                tel2 = datos[3]
                correo = datos[4]
                grupo = datos[5]
                activo = datos[6]
                print(f"{idc:<5}{nombre:<20}{tel1:<15}{tel2:<15}{correo:<25}{grupo:<10}{activo:<10}")
            linea = arch.readline()
    finally:
        try:
            arch.close()
        except NameError as mensaje:
            print("Se ha producido un error:", mensaje)



def listar_contactos_linea_base(incluir_anulados=False):
    try:
        arch = open(RUTA_ARCHIVO_CONTACTO, "rt", encoding="UTF-8")
    except OSError as error:
        print(f"No se pudo leer el archivo {RUTA_ARCHIVO_CONTACTO}: {error}")
    else:
        print("\n=== LISTADO DE CONTACTOS ===")
        print(f'{"ID":<5}{"NOMBRE":<20}{"ACTIVO":<10}')
        linea = arch.readline()
        hay_contactos = False

        while linea != "":
            datos = linea.strip().split(";")
            if len(datos) >= 7:
                idc = datos[0]
                nombre = datos[1]
                activo = datos[6].strip().lower()

                # Mostrar según parámetro incluir_anulados
                if activo == "true" or incluir_anulados:
                    print(f"{idc:<5}{nombre:<20}{activo:<10}")
                    hay_contactos = True

            linea = arch.readline()

        if not hay_contactos:
            print("(no hay contactos a mostrar)")
    finally:
        try:
            arch.close()
        except NameError as mensaje:
            print("Se ha producido un error:", mensaje)


def filtrar_contactos(filtro_nombre="", filtro_grupo_desc="", ruta_contactos="", ruta_grupos=""):
    try:
        arch = open(ruta_contactos, "rt", encoding="UTF-8")
    except OSError as error:
        print(f"No se pudo abrir el archivo {ruta_contactos}: {error}")
        return []
    else:
        resultados = []
        linea = arch.readline()
        while linea != "":
            datos = linea.strip().split(";")
            if len(datos) >= 7:
                idc = datos[0]
                nombre = datos[1]
                tel1 = datos[2]
                tel2 = datos[3]
                correo = datos[4]
                id_grupo = datos[5]
                activo = datos[6].strip().lower()

                if activo == "true":
                    cumple_filtro = True

                    if filtro_nombre.strip() != "" and filtro_nombre.lower() not in nombre.lower():
                        cumple_filtro = False

                    if filtro_grupo_desc.strip() != "":
                        try:
                            gfile = open(ruta_grupos, "rt", encoding="UTF-8")
                            grupo_nombre = "(sin grupo)"
                            linea_grupo = gfile.readline()
                            while linea_grupo != "":
                                gdatos = linea_grupo.strip().split(";")
                                if len(gdatos) >= 3 and gdatos[0] == id_grupo:
                                    grupo_nombre = gdatos[1]
                                    break
                                linea_grupo = gfile.readline()
                            gfile.close()

                            if filtro_grupo_desc.lower() not in grupo_nombre.lower():
                                cumple_filtro = False
                        except OSError:
                            cumple_filtro = False

                    if cumple_filtro:
                        resultados.append([idc, nombre, tel1, tel2, correo, id_grupo, activo])
            linea = arch.readline()
        return resultados
    finally:
        try:
            arch.close()
        except NameError as mensaje:
            print("Se ha producido un error:", mensaje)

def baja_contacto():
    """
    Permite eliminar un contacto (baja lógica o física).
    Lee y escribe sobre archivo JSON.
    """
    if not os.path.exists(RUTA_ARCHIVO_CONTACTO) or os.path.getsize(RUTA_ARCHIVO_CONTACTO) == 0:
        print("No hay contactos registrados.")
        return

    try:
        with open(RUTA_ARCHIVO_CONTACTO, "r", encoding="UTF-8") as archivo:
            contactos = json.load(archivo)
    except (OSError, json.JSONDecodeError):
        print("Error al leer el archivo de contactos.")
        return

    # Mostrar contactos activos antes de eliminar
    contactos_activos = [c for c in contactos if c.get("activo", True)]
    if not contactos_activos:
        print("No hay contactos activos para eliminar.")
        return

    print("\nID | NOMBRE                | TELÉFONO PRINCIPAL")
    print("-----------------------------------------------")
    for c in contactos_activos:
        print(f"{str(c['id']).ljust(2)} | {c['nombre'].ljust(20)} | {c['tel1']}")

    codigo_baja = input("\nIngrese el ID del contacto a eliminar: ").strip()

    encontrado = False
    for c in contactos:
        if str(c["id"]) == codigo_baja and c.get("activo", True):
            encontrado = True
            print(f"\nContacto encontrado: {c['id']} - {c['nombre']}")
            confirmar = input("¿Desea eliminarlo permanentemente? (s/n): ").strip().lower()

            if confirmar == "s":
                contactos.remove(c)
                print("Contacto eliminado permanentemente.")
            else:
                c["activo"] = False
                print("Contacto marcado como inactivo (baja lógica).")
            break

    if not encontrado:
        print(f"No se encontró un contacto activo con el ID {codigo_baja}.")
        return

    try:
        with open(RUTA_ARCHIVO_CONTACTO, "w", encoding="UTF-8") as archivo:
            json.dump(contactos, archivo, ensure_ascii=False, indent=4)
        print("Operación completada correctamente.")
    except OSError as e:
        print("Error al escribir el archivo:", e)


def _ingresar_id_contacto():
    while True:
        try:
            entrada = int(input("Ingrese ID de contacto: ").strip())
            return entrada
        except ValueError:
            print("ID inválido. Debe ser numérico.")

def modificar_contacto():
    
    codigo_modif = _ingresar_id_contacto()
    encontrado = False

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
            print("No se pudo cerrar el archivo:", e)

    for c in contactos:
        if c["id"] == codigo_modif:
            encontrado = True
            print(f"\nContacto encontrado: {c['id']} - {c['nombre']}")
            print("Deje vacío para mantener el valor actual.\n")

            nuevo_nombre = input(f"Nombre ({c['nombre']}): ").strip()
            nuevo_tel1 = input(f"Teléfono 1 ({c['tel1']}): ").strip()
            nuevo_tel2 = input(f"Teléfono 2 ({c['tel2']}): ").strip()
            nuevo_correo = input(f"Correo ({c['correo']}): ").strip()
            nuevo_grupo = input(f"ID Grupo ({c['id_grupo']}): ").strip()

            if nuevo_nombre != "":
                c["nombre"] = nuevo_nombre
            if nuevo_tel1 != "":
                c["tel1"] = nuevo_tel1
            if nuevo_tel2 != "":
                c["tel2"] = nuevo_tel2
            if nuevo_correo != "":
                c["correo"] = nuevo_correo
            if nuevo_grupo != "":
                try:
                    c["id_grupo"] = int(nuevo_grupo)
                except ValueError:
                    print("El ID de grupo debe ser numérico. Se mantiene el valor anterior.")

            print("Contacto modificado correctamente.")
            break

    if not encontrado:
        print(f"No se encontró el contacto con ID {codigo_modif}.")
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
            print("No se pudo cerrar el archivo:", e)



def telefonos_unicos():
    telefonos = set()
    try:
        with open(RUTA_ARCHIVO_CONTACTO, "rt", encoding="UTF-8") as arch:
            linea = arch.readline()
            while linea != "":
                datos = linea.strip().split(";")
                if len(datos) >= 7:
                    tel1 = datos[2].strip()
                    tel2 = datos[3].strip()
                    activo = datos[6].strip().lower()

                    if activo == "true":
                        if tel1 != "":
                            telefonos.add(tel1)
                        if tel2 != "":
                            telefonos.add(tel2)
                linea = arch.readline()
    except OSError as error:
        print(f"No se pudo leer el archivo de contactos: {error}")

    return telefonos


"""
TIPO DE INTERACIONES
    "
"""
def listar_tipos():
    try:
        with open(RUTA_ARCHIVO_TIPOS, "rt", encoding="UTF-8") as arch:
            print("\n=== LISTADO DE TIPOS DE INTERACCIÓN ===")
            print(f'{"ID":<5}{"DESCRIPCIÓN":<20}')
            print("-----------------------------------")

            for linea in arch:
                datos = linea.strip().split(";")
                if len(datos) >= 2:
                    print(f"{datos[0]:<5}{datos[1]:<20}")

    except OSError as error:
        print(f"No se pudo leer el archivo: {error}")



def next_id_tipos():
   
    if not os.path.exists(RUTA_ARCHIVO_TIPOS) or os.path.getsize(RUTA_ARCHIVO_TIPOS) == 0:
        return 1

    with open(RUTA_ARCHIVO_TIPOS, "rt", encoding="UTF-8") as arch:
        ids = []
        for linea in arch:
            datos = linea.strip().split(";")
            if len(datos) >= 1 and datos[0].isdigit():
                ids.append(int(datos[0]))

    return max(ids, default=0) + 1

def alta_tipo():
    nuevo_id = next_id_tipos()
    descripcion = input("Ingrese descripción del tipo: ").strip()

    try:
        with open(RUTA_ARCHIVO_TIPOS, "at", encoding="UTF-8") as arch:
            arch.write(f"{nuevo_id};{descripcion}\n")
            print(f"Tipo '{descripcion}' agregado correctamente.")
    except OSError as error:
        print("Error al escribir en el archivo:", error)


def baja_tipo():
    codigo_baja = input("Ingrese el ID del tipo a eliminar: ").strip()
    temp = "temp.txt"
    encontrado = False

    try:
        with open(RUTA_ARCHIVO_TIPOS, "rt", encoding="UTF-8") as arch, \
             open(temp, "wt", encoding="UTF-8") as aux:

            for linea in arch:
                datos = linea.strip().split(";")
                codigo = datos[0]
                if codigo != codigo_baja:
                    aux.write(linea)
                else:
                    encontrado = True

    except FileNotFoundError:
        print("El archivo no existe.")
    except OSError as error:
        print("Error en el acceso al archivo:", error)

    if encontrado:
        os.remove(RUTA_ARCHIVO_TIPOS)
        os.rename(temp, RUTA_ARCHIVO_TIPOS)
        print(f"Tipo {codigo_baja} eliminado correctamente.")
    else:
        os.remove(temp)
        print(f"No se encontró el tipo {codigo_baja}.")


def modificar_tipo():
    codigo_modif = input("Ingrese el ID del tipo a modificar: ").strip()
    temp = "temp.txt"
    encontrado = False

    try:
        with open(RUTA_ARCHIVO_TIPOS, "rt", encoding="UTF-8") as arch, \
             open(temp, "wt", encoding="UTF-8") as aux:

            for linea in arch:
                datos = linea.strip().split(";")
                codigo = datos[0]
                if codigo == codigo_modif:
                    encontrado = True
                    descripcion = datos[1]
                    print(f"Tipo encontrado: {codigo} - {descripcion}")
                    nueva_desc = input("Nueva descripción (Enter para mantener): ").strip() or descripcion
                    aux.write(f"{codigo};{nueva_desc}\n")
                    print(f"Tipo {codigo} modificado correctamente.")
                else:
                    aux.write(linea)

    except FileNotFoundError:
        print("El archivo no existe.")
    except OSError as error:
        print("Error en el acceso al archivo:", error)

    if encontrado:
        os.remove(RUTA_ARCHIVO_TIPOS)
        os.rename(temp, RUTA_ARCHIVO_TIPOS)
    else:
        os.remove(temp)
        print(f"No se encontró el tipo {codigo_modif}.")


def elegir_tipo_interaccion():
    try:
        with open(RUTA_ARCHIVO_TIPOS, "rt", encoding="UTF-8") as arch:
            print("\n=== TIPOS DE INTERACCIÓN ===")
            tipos = {}

            for linea in arch:
                datos = linea.strip().split(";")
                if len(datos) >= 2:
                    codigo = datos[0]
                    descripcion = datos[1]
                    tipos[codigo] = descripcion
                    print(f"{codigo}: {descripcion}")

    except OSError as error:
        print(f"No se pudo abrir el archivo de tipos: {error}")
        return None

    opcion = input("\nSeleccione el ID del tipo de interacción: ").strip()
    if opcion in tipos:
        return tipos[opcion]
    else:
        print("Opción inválida.")
        return None


"""
ionterraciones
"""

# --------------------------------------------------------
# AGREGAR INTERACCIÓN
# --------------------------------------------------------
def agregar_datosInteraccion(nueva_interaccion):
    
    try:
        arch = open(RUTA_ARCHIVO_INTERACCIONES, "at", encoding="UTF-8")
        linea = f"{nueva_interaccion['id']};{nueva_interaccion['id_contacto']};{nueva_interaccion['descripcion']};{nueva_interaccion['fecha']};{nueva_interaccion['tipo']};{nueva_interaccion['anulado']}\n"
        arch.write(linea)
        print(f"Interacción registrada correctamente (ID {nueva_interaccion['id']}).")
        arch.close()
    except OSError as error:
        print("Error al escribir el archivo:", error)


# --------------------------------------------------------
# CALCULAR PRÓXIMO ID
# --------------------------------------------------------
def next_id_interaccion():
   
    if not os.path.exists(RUTA_ARCHIVO_INTERACCIONES):
        return 1
    try:
        arch = open(RUTA_ARCHIVO_INTERACCIONES, "rt", encoding="UTF-8")
        ultimo = 0
        for linea in arch:
            datos = linea.strip().split(";")
            if len(datos) > 0 and datos[0].isdigit():
                if int(datos[0]) > ultimo:
                    ultimo = int(datos[0])
        arch.close()
        return ultimo + 1
    except OSError:
        return 1


# --------------------------------------------------------
# LISTAR INTERACCIONES
# --------------------------------------------------------
def leer_interacciones(incluir_anuladas=False):
    filas = []
    if not os.path.exists(RUTA_ARCHIVO_INTERACCIONES):
        return filas

    try:
        arch = open(RUTA_ARCHIVO_INTERACCIONES, "rt", encoding="UTF-8")
        for linea in arch:
            datos = linea.strip().split(";")
            if len(datos) < 6:
                continue
            activo = datos[5].lower()
            if activo == "false" or incluir_anuladas:
                filas.append({
                    "id": datos[0],
                    "id_contacto": datos[1],
                    "descripcion": datos[2],
                    "fecha": datos[3],
                    "tipo": datos[4],
                    "activo": activo
                })
        arch.close()
    except OSError as e:
        print("Error al leer el archivo:", e)

    return filas


# --------------------------------------------------------
# MODIFICAR INTERACCIÓN
# --------------------------------------------------------
def modificar_interaccion():
    codigo = input("Ingrese el ID de la interacción a modificar: ").strip()
    if codigo == "":
        print("ID inválido.")
        return

    if not os.path.exists(RUTA_ARCHIVO_INTERACCIONES):
        print("No existe el archivo de interacciones.")
        return

    arch = open(RUTA_ARCHIVO_INTERACCIONES, "rt", encoding="UTF-8")
    aux = open("temp.txt", "wt", encoding="UTF-8")
    encontrado = False

    for linea in arch:
        datos = linea.strip().split(";")
        if len(datos) < 6:
            continue
        if datos[0] == codigo:
            encontrado = True
            idc, desc, fecha, tipo, activo = datos[1], datos[2], datos[3], datos[4], datos[5]
            print(f"Interacción: {codigo} - {desc} ({fecha}) - {tipo}")
            nueva_desc = input("Nueva descripción (Enter para mantener): ").strip() or desc
            nueva_fecha = input("Nueva fecha (Enter para mantener): ").strip() or fecha
            nuevo_tipo = input("Nuevo tipo (Enter para mantener): ").strip() or tipo
            aux.write(f"{codigo};{idc};{nueva_desc};{nueva_fecha};{nuevo_tipo};{activo}\n")
            print("Interacción modificada.")
        else:
            aux.write(linea)

    arch.close()
    aux.close()

    if encontrado:
        os.remove(RUTA_ARCHIVO_INTERACCIONES)
        os.rename("temp.txt", RUTA_ARCHIVO_INTERACCIONES)
    else:
        os.remove("temp.txt")
        print("No se encontró la interacción.")


# --------------------------------------------------------
# ELIMINAR INTERACCIÓN
# --------------------------------------------------------
def eliminar_interaccion():
    codigo = input("Ingrese el ID de la interacción a eliminar: ").strip()
    if codigo == "":
        print("ID inválido.")
        return

    if not os.path.exists(RUTA_ARCHIVO_INTERACCIONES):
        print("No existe el archivo de interacciones.")
        return

    arch = open(RUTA_ARCHIVO_INTERACCIONES, "rt", encoding="UTF-8")
    aux = open("temp.txt", "wt", encoding="UTF-8")
    encontrado = False

    for linea in arch:
        datos = linea.strip().split(";")
        if len(datos) < 6:
            continue
        if datos[0] == codigo:
            encontrado = True
            idc, desc, fecha, tipo, activo = datos[1], datos[2], datos[3], datos[4], datos[5]
            print(f"Interacción: {codigo} - {desc} ({fecha}) - {tipo}")
            op = input("¿Eliminar definitivamente (F) o marcar como anulada (L)? [F/L]: ").strip().lower()
            if op == "f":
                print("Interacción eliminada definitivamente.")
            else:
                aux.write(f"{codigo};{idc};{desc};{fecha};{tipo};false\n")
                print("Interacción marcada como anulada.")
        else:
            aux.write(linea)

    arch.close()
    aux.close()

    if encontrado:
        os.remove(RUTA_ARCHIVO_INTERACCIONES)
        os.rename("temp.txt", RUTA_ARCHIVO_INTERACCIONES)
    else:
        os.remove("temp.txt")
        print("No se encontró la interacción.")


# --------------------------------------------------------
# RESTAURAR INTERACCIÓN
# --------------------------------------------------------
def restaurar_interaccion():
    codigo = input("Ingrese el ID de la interacción a restaurar: ").strip()
    if codigo == "":
        print("ID inválido.")
        return

    if not os.path.exists(RUTA_ARCHIVO_INTERACCIONES):
        print("No existe el archivo de interacciones.")
        return

    arch = open(RUTA_ARCHIVO_INTERACCIONES, "rt", encoding="UTF-8")
    aux = open("temp.txt", "wt", encoding="UTF-8")
    encontrado = False

    for linea in arch:
        datos = linea.strip().split(";")
        if len(datos) < 6:
            continue
        if datos[0] == codigo and datos[5].strip().lower() == "false":
            encontrado = True
            aux.write(f"{datos[0]};{datos[1]};{datos[2]};{datos[3]};{datos[4]};true\n")
            print("Interacción restaurada correctamente.")
        else:
            aux.write(linea)

    arch.close()
    aux.close()

    if encontrado:
        os.remove(RUTA_ARCHIVO_INTERACCIONES)
        os.rename("temp.txt", RUTA_ARCHIVO_INTERACCIONES)
    else:
        os.remove("temp.txt")
        print("No se encontró una interacción anulada con ese ID.")