RUTA_ARCHIVO = r"C:\Users\fsotelo\Desktop\MATERIAS\2DO Cuatrimestre\PROGRAMACION I\Integrador Contactos\contacto.txt"

def guardar_contacto(contacto):
    try:
        arch = open(RUTA_ARCHIVO, "a", encoding="UTF-8")
        linea = ";".join(str(c) for c in contacto) + "\n"
        arch.write(linea)
        print("Contacto guardado en archivo correctamente.")
    except OSError as e:
        print("No se puede grabar el archivo:", e)
    finally:
        try:
            arch.close()
        except NameError:
            pass