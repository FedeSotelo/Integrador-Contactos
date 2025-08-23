from contacto import alta_contacto, listar_contactos_detallado
from grupo import listar_grupos

def menu():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Alta de contacto")
        print("2. Listar contactos")
        print("3. Listar grupos")
        print("0. Salir")

        opcion = input("Opción: ")

        if opcion == "1":
            alta_contacto()
        elif opcion == "2":
            listar_contactos_detallado()
        elif opcion == "3":
            listar_grupos()
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

menu()
