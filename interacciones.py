from contacto import contactos,_buscar_contacto_index_por_id, listar_contactos_detallado
from grupo import crear_grupo_interactivo

interacciones = []

tipoInteraccion = ["llamada", "mensaje", "email", "reunión", "videollamada", "otro"]

def next_id(lista):
    if len(lista) == 0:
        return 1
    ids = [fila[0] for fila in lista]
    return max(ids) + 1


def elegir_Contacto(filtroNombre: str = "" , filtroGrupoDesc: str = ""):
    while True:
        contactos_filtrados = listar_contactos_detallado(filtroNombre, filtroGrupoDesc)
        if len(contactos_filtrados) == 0:
            print("No hay contactos.")          
            return None

        entrada = input("Ingrese id del contacto: ").strip()
        if entrada.isdigit():
            val = int(entrada)
            g = _buscar_contacto_index_por_id(val)
            if g != -1:
                return val
        print("Opción inválida.")

       

def  crear_interaccion():
    filtro_nombre = input("Filtrar por nombre (enter para todos): ").strip()
    filtro_grupo_desc = input("Filtrar por grupo (descripción, enter para todos): ").strip()
    idContacto = elegir_Contacto(filtro_nombre, filtro_grupo_desc)

    if idContacto is None:
        print("No se seleccionó ningún contacto.")
        return

    idx = _buscar_contacto_index_por_id(int(idContacto))
    if idx == -1:
        print("No existe un contacto con ese ID.")
        return

    descripcion = input("Descripcion: ").strip()
    while descripcion == "" or not descripcion.replace(" ", "").isalpha():
        print("La descripcion es opcional y debe contener solo letras.")
        descripcion = input("Descripcion (opcional): ").strip()

    fecha = input("Fecha (DD/MM/AAAA): ").strip()

    tipoInteraccion = ["llamada", "mensaje", "email", "reunión", "videollamada", "otro"]
    tipo = input(f"Tipo de interacción ({', '.join(tipoInteraccion)}): ").strip().lower()
    while tipo not in tipoInteraccion:
        print("Tipo de interacción no válido.")
        tipo = input(f"Tipo de interacción ({', '.join(tipoInteraccion)}): ").strip().lower()

    iId = next_id(interacciones)
    interacciones.append([iId, idContacto, descripcion, fecha, tipo])
    print("Interacción creada con éxito.")






