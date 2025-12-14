"""
-----------------------------------------------------------------------------------------------
Título: Gestor de Contactos
Fecha: 25/08/2025
Autor: ramiro balmaceda, santino pota, santiago ruiz, Federico sotelo, luka subotovksy,

Descripcion:
Sistema de gestion de contactos, grupos e interacciones con menus navegables.

Pendientes:

-----------------------------------------------------------------------------------------------
"""

#----------------------------------------------------------------------------------------------
# MODULOS
#----------------------------------------------------------------------------------------------
from colorama import Fore, Back, Style, init

# Inicializar colorama
init(autoreset=True)

from contacto import (
    listar_contactos_detallado,
    alta_contacto,
    eliminar_contacto,   
    editar_contacto, 
    restaurar_contacto
)
from grupo import (
    listar_grupos,
    crear_grupo_interactivo,
    eliminar_grupo,      
    editar_grupo,
    buscar_grupo_por_id   
)
from interacciones import (
    crear_interaccion,
    listar_interacciones,
    editar_interaccion,
    eliminar_interaccion,
    restaurar_interaccion,
    ver_historial_por_contacto,
    ver_historial_por_grupo,
    listar_tipos,
    alta_tipo,
    baja_tipo,
    modificar_tipo
)

from estadisticas import (
    cantidad_contactos_por_grupo,
    promedio_interacciones_por_contacto,
    porcentaje_contactos_activos,
    contacto_con_mas_y_menos_interacciones,
    matriz_contactos_por_grupo_y_tipo
)

from login import login

#----------------------------------------------------------------------------------------------
# FUNCIONES
#----------------------------------------------------------------------------------------------
def limpiar_pantalla():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_contactos():
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + "\n╔══════════════════════════════════╗")
        print(Fore.CYAN + "║         " + Fore.YELLOW + "CONTACTOS" + Fore.CYAN + "                ║")
        print(Fore.CYAN + "╚══════════════════════════════════╝" + Style.RESET_ALL)
        print(Fore.GREEN + "1)" + Style.RESET_ALL + " Despliegue de lista (con filtros)")
        print(Fore.GREEN + "2)" + Style.RESET_ALL + " Agregar contacto")
        print(Fore.GREEN + "3)" + Style.RESET_ALL + " Eliminar contacto")
        print(Fore.GREEN + "4)" + Style.RESET_ALL + " Editar contacto")
        print(Fore.GREEN + "5)" + Style.RESET_ALL + " Restaurar contacto")
        print(Fore.RED + "0)" + Style.RESET_ALL + " Volver")
        
        op = input(Fore.CYAN + "\nOpcion: " + Style.RESET_ALL).strip()
        
        if op == "1":
            filtro_nombre = input("Filtrar por nombre (enter para todos): ")
            filtro_grupo_desc = input("Filtrar por grupo (descripcion, enter para todos): ")
            listar_contactos_detallado(
                filtro_nombre=filtro_nombre,
                filtro_grupo_desc=filtro_grupo_desc
            )
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "2":
            alta_contacto()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "3":
            eliminar_contacto()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "4":
            editar_contacto()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "5":
            restaurar_contacto()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "0":
            break
        else:
            print(Fore.RED + "Opcion invalida." + Style.RESET_ALL)
            input(Fore.YELLOW + "Presione ENTER para continuar..." + Style.RESET_ALL)


def menu_grupos():
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + "\n╔══════════════════════════════════╗")
        print(Fore.CYAN + "║           " + Fore.YELLOW + "GRUPOS" + Fore.CYAN + "                 ║")
        print(Fore.CYAN + "╚══════════════════════════════════╝" + Style.RESET_ALL)
        print(Fore.GREEN + "1)" + Style.RESET_ALL + " Despliegue de lista")
        print(Fore.GREEN + "2)" + Style.RESET_ALL + " Crear grupo")
        print(Fore.GREEN + "3)" + Style.RESET_ALL + " Eliminar grupo")
        print(Fore.GREEN + "4)" + Style.RESET_ALL + " Editar grupo")
        print(Fore.RED + "0)" + Style.RESET_ALL + " Volver")
        
        op = input(Fore.CYAN + "\nOpcion: " + Style.RESET_ALL).strip()
        
        if op == "1":
            listar_grupos()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "2":
            crear_grupo_interactivo()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "3":
            eliminar_grupo()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "4":
            editar_grupo()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "0":
            break
        else:
            print(Fore.RED + "Opcion invalida." + Style.RESET_ALL)
            input(Fore.YELLOW + "Presione ENTER para continuar..." + Style.RESET_ALL)


def menu_interacciones():
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + "\n╔══════════════════════════════════╗")
        print(Fore.CYAN + "║       " + Fore.YELLOW + "INTERACCIONES" + Fore.CYAN + "              ║")
        print(Fore.CYAN + "╚══════════════════════════════════╝" + Style.RESET_ALL)
        print(Fore.GREEN + "1)" + Style.RESET_ALL + " Despliegue de lista")
        print(Fore.GREEN + "2)" + Style.RESET_ALL + " Crear una interacción")
        print(Fore.GREEN + "3)" + Style.RESET_ALL + " Editar interacción")
        print(Fore.GREEN + "4)" + Style.RESET_ALL + " Eliminar interacción")
        print(Fore.GREEN + "5)" + Style.RESET_ALL + " Restaurar interacción")
        print(Fore.GREEN + "6)" + Style.RESET_ALL + " Ver historial por contacto")
        print(Fore.GREEN + "7)" + Style.RESET_ALL + " Ver historial por grupo")
        print(Fore.GREEN + "8)" + Style.RESET_ALL + " Tipos de interacción")
        print(Fore.RED + "0)" + Style.RESET_ALL + " Volver")

        op = input(Fore.CYAN + "\nOpción: " + Style.RESET_ALL).strip()
        
        if op == "1":
            listar_interacciones()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "2":
            crear_interaccion()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "3":
            editar_interaccion()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "4":
            eliminar_interaccion()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "5":
            restaurar_interaccion()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "6":
            ver_historial_por_contacto()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "7":
            ver_historial_por_grupo()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "8":
            menu_tipos()
        elif op == "0":
            break
        else:
            print(Fore.RED + "Opción inválida." + Style.RESET_ALL)
            input(Fore.YELLOW + "Presione ENTER para continuar..." + Style.RESET_ALL)

def menu_tipos():
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + "\n╔══════════════════════════════════╗")
        print(Fore.CYAN + "║    " + Fore.YELLOW + "TIPOS DE INTERACCIÓN" + Fore.CYAN + "         ║")
        print(Fore.CYAN + "╚══════════════════════════════════╝" + Style.RESET_ALL)
        print(Fore.GREEN + "1)" + Style.RESET_ALL + " Listar tipos")
        print(Fore.GREEN + "2)" + Style.RESET_ALL + " Agregar tipo")
        print(Fore.GREEN + "3)" + Style.RESET_ALL + " Modificar tipo")
        print(Fore.GREEN + "4)" + Style.RESET_ALL + " Eliminar tipo")
        print(Fore.RED + "0)" + Style.RESET_ALL + " Volver")

        op = input(Fore.CYAN + "\nOpción: " + Style.RESET_ALL).strip()

        if op == "1":
            listar_tipos()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "2":
            alta_tipo()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "3":
            modificar_tipo()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "4":
            baja_tipo()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "0":
            break
        else:
            print(Fore.RED + "Opción inválida." + Style.RESET_ALL)
            input(Fore.YELLOW + "Presione ENTER para continuar..." + Style.RESET_ALL)


def menu_estadisticas():
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + "\n╔══════════════════════════════════╗")
        print(Fore.CYAN + "║        " + Fore.YELLOW + "ESTADISTICAS" + Fore.CYAN + "              ║")
        print(Fore.CYAN + "╚══════════════════════════════════╝" + Style.RESET_ALL)
        print(Fore.GREEN + "1)" + Style.RESET_ALL + " Cantidad de contactos por grupo")
        print(Fore.GREEN + "2)" + Style.RESET_ALL + " Promedio de interacciones por contacto")
        print(Fore.GREEN + "3)" + Style.RESET_ALL + " Porcentaje de contactos activos")
        print(Fore.GREEN + "4)" + Style.RESET_ALL + " Contacto con más y menos interacciones")
        print(Fore.GREEN + "5)" + Style.RESET_ALL + " Matriz de interacciones por grupo y tipo")
        print(Fore.RED + "0)" + Style.RESET_ALL + " Volver")

        op = input(Fore.CYAN + "\nOpcion: " + Style.RESET_ALL).strip()

        if op == "1":
            cantidad_contactos_por_grupo()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "2":
            promedio_interacciones_por_contacto()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "3":
            porcentaje_contactos_activos()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "4":
            contacto_con_mas_y_menos_interacciones()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "5":
            matriz_contactos_por_grupo_y_tipo()
            input(Fore.YELLOW + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        elif op == "0":
            break
        else:
            print(Fore.RED + "Opcion invalida." + Style.RESET_ALL)
            input(Fore.YELLOW + "Presione ENTER para continuar..." + Style.RESET_ALL)


#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():
    while True:
        limpiar_pantalla()
        print()
        print(Fore.CYAN + "╔══════════════════════════════════╗")
        print(Fore.CYAN + "║    " + Fore.YELLOW + Style.BRIGHT + "MENÚ PRINCIPAL" + Style.RESET_ALL + Fore.CYAN + "                ║")
        print(Fore.CYAN + "║    " + Fore.MAGENTA + "Gestor de Contactos" + Fore.CYAN + "           ║")
        print(Fore.CYAN + "╚══════════════════════════════════╝" + Style.RESET_ALL)
        print()
        print(Fore.GREEN + "[1]" + Style.RESET_ALL + " Gestión de contactos")
        print(Fore.GREEN + "[2]" + Style.RESET_ALL + " Gestión de grupos")
        print(Fore.GREEN + "[3]" + Style.RESET_ALL + " Gestión de interacciones")
        print(Fore.GREEN + "[4]" + Style.RESET_ALL + " Estadísticas")
        print(Fore.GREEN + "[5]" + Style.RESET_ALL + " Cerrar sesión")
        print(Fore.RED + "[0]" + Style.RESET_ALL + " Salir del programa")
        print(Fore.CYAN + "──────────────────────────────────" + Style.RESET_ALL)
        print()
        
        opcion = input(Fore.CYAN + "Seleccione una opción: " + Style.RESET_ALL).strip()
        
        if opcion == "0":
            print(Fore.YELLOW + "\n✓ Saliendo..." + Style.RESET_ALL)
            exit()
        elif opcion == "1":
            menu_contactos()
        elif opcion == "2":
            menu_grupos()
        elif opcion == "3":
            menu_interacciones()
        elif opcion == "4":
            menu_estadisticas()
        elif opcion == "5":
            print(Fore.YELLOW + "\nCerrando sesión...\n" + Style.RESET_ALL)
            if login():   
                continue
        else:
            print(Fore.RED + "\n✗ Opción inválida." + Style.RESET_ALL)
            input(Fore.YELLOW + "Presione ENTER para continuar..." + Style.RESET_ALL)


if login():
    main()  
else:
    print(Fore.RED + "✗ Acceso denegado." + Style.RESET_ALL)