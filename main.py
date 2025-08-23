from contacto import (
    listar_contactos_detallado,
    alta_contacto,
    eliminar_contacto,   
    editar_contacto      
)
from grupo import (
    listar_grupos,
    crear_grupo_interactivo,
    eliminar_grupo,      
    editar_grupo         
)
""" 

from interaccion import (      
)

"""
def menu_contactos():
    while True:
        print("\n=== CONTACTOS ===")
        print("1) Despliegue de lista")
        print("2) Agregar contacto")
        print("3) Eliminar contacto")
        print("4) Editar contacto")
        print("0) Volver")
        op = input("Opción: ").strip()
        if op == "1":
            listar_contactos_detallado()
        elif op == "2":
            alta_contacto()
        elif op == "3":
            eliminar_contacto()
        elif op == "4":
            editar_contacto()
        elif op == "0":
            break
        else:
            print("Opción inválida.")

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
            print("Opción inválida.")
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
            print("Opción inválida.")
"""
def menu_principal():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1) Contactos")
        print("2) Grupos")
        print("3) Interacciones")
        print("0) Salir")
        op = input("Opción: ").strip()
        if op == "1":
            menu_contactos()
        elif op == "2":
            menu_grupos()
            """""
        elif op == "3":
            menu_interacciones()
            """
        elif op == "0":
            print("Saliendo…")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu_principal()
