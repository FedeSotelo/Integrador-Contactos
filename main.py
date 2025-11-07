"""
-----------------------------------------------------------------------------------------------
Título: Gestor de Contactos
Fecha: 25/08/2025
Autor:  ramiro balmaceda, santino pota, santiago ruiz, Federico sotelo, luka subotovksy,

Descripcion:
Sistema de gestion de contactos, grupos e interacciones con menus navegables.

Pendientes:

-----------------------------------------------------------------------------------------------
"""

#----------------------------------------------------------------------------------------------
# MODULOS
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
from estadisticas import (
    cantidad_contactos_por_grupo,
    promedio_interacciones_por_contacto,
    porcentaje_contactos_activos
)

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
        op = input("Opcion: ").strip()
        if op == "1":
            filtro_nombre = input("Filtrar por nombre (enter para todos): ")
            filtro_grupo_desc = input("Filtrar por grupo (descripcion, enter para todos): ")
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
            input("Opcion invalida. Presione ENTER para continuar.")


def menu_grupos():
    while True:
        print("\n=== GRUPOS ===")
        print("1) Despliegue de lista")
        print("2) Crear grupo")
        print("3) Eliminar grupo")
        print("4) Editar grupo")
        print("0) Volver")
        op = input("Opcion: ").strip()
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
            input("Opcion invalida. Presione ENTER para continuar.")


def menu_interacciones():
    while True:
        print("\n=== INTERACCIONES ===")
        print("1) Despliegue de lista")
        print("2) Crear una interacción")
        print("3) Editar interacción")
        print("4) Eliminar interacción")
        print("5) Restaurar interacción")
        print("6) Ver historial por contacto")
        print("7) Ver historial por grupo")
        print("8) Tipos de interacción")  # <- agregá esta línea
        print("0) Volver")

        op = input("Opción: ").strip()
        if op == "1":
            listar_interacciones()
        elif op == "2":
            crear_interaccion()
        elif op == "3":
            editar_interaccion()
        elif op == "4":
            eliminar_interaccion()
        elif op == "5":
            restaurar_interaccion()
        elif op == "6":
            ver_historial_por_contacto()
        elif op == "7":
            ver_historial_por_grupo()
        elif op == "8":
            menu_tipos() 
        elif op == "0":
            break
        else:
            input("Opción inválida. Presione ENTER para continuar.")

def menu_tipos():
    while True:
        print("\n=== TIPOS DE INTERACCIÓN ===")
        print("1) Listar tipos")
        print("2) Agregar tipo")
        print("3) Modificar tipo")
        print("4) Eliminar tipo")
        print("0) Volver")

        op = input("Opción: ").strip()

        if op == "1":
            listar_tipos()
        elif op == "2":
            alta_tipo()
        elif op == "3":
            modificar_tipo()
        elif op == "4":
            baja_tipo()
        elif op == "0":
            break
        else:
            input("Opción inválida. Presione ENTER para continuar.")


def menu_estadisticas():
    while True:
        print("\n=== ESTADISTICAS ===")
        print("1) Cantidad de contactos por grupo")
        print("2) Promedio de interacciones por contacto")
        print("3) Porcentaje de contactos activos")
        print("4) Contacto con mas y menos interacciones")
        print("5) Matriz de interacciones por grupo y tipo")   
        print("0) Volver")

        op = input("Opcion: ").strip()

        if op == "1":
            cantidad_contactos_por_grupo()
        elif op == "2":
            promedio_interacciones_por_contacto()
        elif op == "3":
            porcentaje_contactos_activos()
        elif op == "4":
            contacto_con_mas_y_menos_interacciones()   
        elif op == "5":
            matriz_contactos_por_grupo_y_tipo()        
        elif op == "0":
            break
        else:
            input("Opcion invalida. Presione ENTER para continuar.")



#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():
    while True:
        print()
        print("---------------------------")
        print("MENÚ PRINCIPAL")
        print("---------------------------")
        print("[1] Gestion de contactos")
        print("[2] Gestion de grupos")
        print("[3] Gestion de interacciones")
        print("[4] Estadisticas")
        print("[5] Cerrar sesion")
        print("---------------------------")
        print("[0] Salir del programa")
        print("---------------------------")
        print()
        
        opcion = input("Seleccione una opcion: ").strip()
        if opcion == "0":
            print("Saliendo…")
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
            print("Cerrando sesion...\n")
            if login():   
                continue
        else:
            input("Opcion invalida. Presione ENTER para continuar.")


if login():
    main()  
else:
    print("Acceso denegado.")
