"""
-----------------------------------------------------------------------------------------------
Título: Gestor de Contactos
Fecha: 25/08/2025
Autor:  ramiro balmaceda, santino pota, santiago ruiz, Federico sotelo, luka subotovksy,

Descripción:
Sistema de gestión de contactos, grupos e interacciones con menús navegables.

Pendientes:

-----------------------------------------------------------------------------------------------
"""

#----------------------------------------------------------------------------------------------
# MÓDULOS
#----------------------------------------------------------------------------------------------
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

"""
from interaccion import (      
    listar_interacciones,
    crear_interaccion,
    ver_historial_por_contacto,
    ver_historial_por_grupo
)
"""

#----------------------------------------------------------------------------------------------
# FUNCIONES
#----------------------------------------------------------------------------------------------
def menu_contactos():
    while True:
        print("\n=== CONTACTOS ===")
        print("1) Despliegue de lista (con filtros)")
        print("2) Agregar contacto")
        print("3) Eliminar contacto")
        print("4) Editar contacto")
        print("5) Restaurar contacto")
        print("0) Volver")
        op = input("Opción: ").strip()
        if op == "1":
            filtro_nombre = input("Filtrar por nombre (enter para todos): ").strip()
            filtro_grupo_desc = input("Filtrar por grupo (descripción, enter para todos): ").strip()
            listar_contactos_detallado(
                filtro_nombre=filtro_nombre,
                filtro_grupo_desc=filtro_grupo_desc
            )
        elif op == "2":
            alta_contacto()
        elif op == "3":
            eliminar_contacto()
        elif op == "4":
            editar_contacto()
        elif op == "5":
            restaurar_contacto()
        elif op == "0":
            break
        else:
            input("Opción inválida. Presione ENTER para continuar.")


def menu_grupos():
    while True:
        print("\n=== GRUPOS ===")
        print("1) Despliegue de lista")
        print("2) Crear grupo")
        print("3) Eliminar grupo")
        print("4) Editar grupo")
        print("0) Volver")
        op = input("Opción: ").strip()
        if op == "1":
            listar_grupos()
        elif op == "2":
            crear_grupo_interactivo()
        elif op == "3":
            eliminar_grupo()
        elif op == "4":
            editar_grupo()
        elif op == "0":
            break
        else:
            input("Opción inválida. Presione ENTER para continuar.")


"""
def menu_interacciones():
    while True:
        print("\n=== INTERACCIONES ===")
        print("1) Despliegue de lista")
        print("2) Crear una interacción")
        print("3) Ver historial por contacto")
        print("4) Ver historial por grupo")
        print("0) Volver")
        op = input("Opción: ").strip()
        if op == "1":
            listar_interacciones()
        elif op == "2":
            crear_interaccion()
        elif op == "3":
            ver_historial_por_contacto()
        elif op == "4":
            ver_historial_por_grupo()
        elif op == "0":
            break
        else:
            input("Opción inválida. Presione ENTER para continuar.")
"""

#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():
    while True:
        while True:
            opciones = 3
            print()
            print("---------------------------")
            print("MENÚ PRINCIPAL")
            print("---------------------------")
            print("[1] Gestión de contactos")
            print("[2] Gestión de grupos")
            print("[3] Gestión de interacciones")
            print("---------------------------")
            print("[0] Salir del programa")
            print("---------------------------")
            print()
            
            opcion = input("Seleccione una opción: ")
            if opcion in [str(i) for i in range(0, opciones + 1)]:
                break
            else:
                input("Opcion inválida. Presione ENTER para volver a seleccionar.")
        print()

        if opcion == "0":
            print("Saliendo…")
            exit()

        elif opcion == "1":
            menu_contactos()
        elif opcion == "2":
            menu_grupos()
        elif opcion == "3":
            print("Interacciones aún no implementadas.")  
            # menu_interacciones()

        input("\nPresione ENTER para volver al menú.")
        print("\n\n")


main()
