RUTA_ARCHIVOContacto = r"C:\Users\fsotelo\Desktop\MATERIAS\2DO Cuatrimestre\PROGRAMACION I\Integrador Contactos\contacto.json"
RUTA_ARCHIVOGrupo = r"C:\Users\fsotelo\Desktop\MATERIAS\2DO Cuatrimestre\PROGRAMACION I\Integrador Contactos\grupo.json"

import json
import os;
def agregar_datosContacto(nuevo_contacto):
    try:
        if os.path.exists(RUTA_ARCHIVOContacto):
            if os.path.getsize(RUTA_ARCHIVOContacto) > 0:
                with open(RUTA_ARCHIVOContacto, 'r', encoding="UTF-8") as datos:
                    contactos = json.load(datos)
            else:
                contactos = []
        else:
            contactos = []

        contactos.append(nuevo_contacto)

        with open(RUTA_ARCHIVOContacto, 'w', encoding="UTF-8") as datos:
            json.dump(contactos, datos, ensure_ascii=False)

        print(f'Se ha agregado el contacto {nuevo_contacto["nombre"]} correctamente.')

    except (FileNotFoundError, OSError) as error:
        print(f'Error: {error}')


def agregar_datosGrupo(nuevo_Grupo):
    try:
        if os.path.exists(RUTA_ARCHIVOGrupo):
            if os.path.getsize(RUTA_ARCHIVOGrupo) > 0:
                with open(RUTA_ARCHIVOGrupo, 'r', encoding="UTF-8") as datos:
                    grupos = json.load(datos)
            else:
                grupos = []
        else:
            grupos = []

        grupos.append(nuevo_Grupo)

        with open(RUTA_ARCHIVOGrupo, 'w', encoding="UTF-8") as datos:
            json.dump(grupos, datos, ensure_ascii=False)

        print(f'Se ha agregado el grupo {nuevo_Grupo["nombre"]} correctamente.')

    except (FileNotFoundError, OSError) as error:
        print(f'Error: {error}')


def baja_contacto():
    codigo_baja = input("Ingrese el ID del contacto a eliminar: ").strip()
    temp = "temp.txt"
    encontrado = False

    try:
        arch = open(RUTA_ARCHIVO, "rt", encoding="UTF-8")
        aux = open(temp, "wt", encoding="UTF-8")

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
    finally:
        try:
            arch.close()
            aux.close()
        except:
            print("Error en el cierre del archivo.")

    if encontrado:
        try:
            os.remove(RUTA_ARCHIVO)
            os.rename(temp, RUTA_ARCHIVO)
            print(f"Contacto {codigo_baja} eliminado correctamente.")
        except OSError as error:
            print("Error al reemplazar el archivo:", error)
    else:
        os.remove(temp)
        print(f"No se encontró el contacto {codigo_baja}.")