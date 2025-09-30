import re
from grupo import grupos_dict, listar_grupos, crear_grupo_interactivo, buscar_grupo_por_id, next_id

# {id: [id, nombre, tel1, tel2, correo, idGrupo, anulado]}
contactos_dict = {}

def validar_correo(c: str) -> bool:
    return (c.strip() == "") or bool(re.match(r"[^@]+@[^@]+\.[^@]+", c))


def obtener_nombre_y_tel(id_contacto):
    """
    esto va devolver una tupla (nombre, telefono) del contacto.
    Si no existe o esta anulado, devuelve none.
    """
    c = contactos_dict.get(id_contacto)
    if c and not c[6]:
        return (c[1], c[2])  # tupla con nombre y tel1
    return None

def _telefonos_unicos():
    """
    Devuelve un conjunto con todos los telefonos unicos (tel1 y tel2) 
    de contactos activos (sin anulados).
    """
    return {
        t
        for c in contactos_dict.values() if not c[6]   # solo contactos activos
        for t in [c[2], c[3]] if t.strip() != ""       # incluye tel1 y tel2 si no están vacíos
    }


def _ingresar_id_contacto():
    while True:
        entrada = input("Ingrese ID de contacto: ").strip()
        if entrada.isdigit():
            return int(entrada)
        print("ID invalido. Debe ser numerico.")

def _listar_contactos_linea_base(incluir_anulados: bool = False):
    filtrados = filter(lambda c: (not c[6]) or incluir_anulados, contactos_dict.values())
    ordenados = sorted(filtrados, key=lambda c: c[0])   # orden por ID
    if len(ordenados) > 0:
        lineas = map(lambda c: f"{str(c[0]).ljust(3)} - {c[1]}", ordenados)
        print("\n".join(lineas))
    else:
        print("(no hay contactos a mostrar)")

def elegir_grupo():
    while True:
        listar_grupos()
        if len(grupos_dict) == 0:
            print("No hay grupos, se creara uno.")
            return crear_grupo_interactivo()

        print("0: Crear grupo nuevo")
        entrada = input("Ingrese id de grupo (o 0): ").strip()
        if entrada.isdigit():
            val = int(entrada)
            if val == 0:
                return crear_grupo_interactivo()
            g = buscar_grupo_por_id(val)
            if g:
                return val
        print("Opcion invalida.")

def alta_contacto():
    print("\n=== Alta de contacto ===")
    nombre = input("Nombre: ").strip()
    while nombre == "" or not nombre.replace(" ", "").isalpha():
        print("El nombre es obligatorio y debe contener solo letras.")
        nombre = input("Nombre (obligatorio): ").strip()

    tel1 = input("Telefono 1: ").strip()
    while tel1 == "" or not tel1.isdigit():
        print("El telefono debe ser numerico y es obligatorio.")
        tel1 = input("Telefono 1 (obligatorio): ").strip()

    if tel1 in _telefonos_unicos():
        print("Este telefono ya existe en otro contacto.")

    tel2 = input("Telefono 2 (opcional): ").strip()
    while tel2 != "" and not tel2.isdigit():
        print("El telefono debe ser numerico o dejar vacío.")
        tel2 = input("Telefono 2 (opcional): ").strip()

    correo = input("Correo (opcional): ").strip()
    while not validar_correo(correo):
        print("Correo invalido.")
        correo = input("Correo (opcional): ").strip()

    id_grupo = elegir_grupo()

    cid = max(contactos_dict.keys(), default=0) + 1

    nuevo = [cid, nombre, tel1, tel2, correo, id_grupo, False]
    contactos_dict[cid] = nuevo

    print(f"Contacto creado con exito (id={cid})")


def listar_contactos_detallado(filtro_nombre: str = "", filtro_grupo_desc: str = ""):
    activos = [c for c in contactos_dict.values() if not c[6]]

    if filtro_nombre.strip() != "":
        activos = [c for c in activos if filtro_nombre.lower() in c[1].lower()]

    if filtro_grupo_desc.strip() != "":
        activos = [c for c in activos if buscar_grupo_por_id(c[5]) and filtro_grupo_desc.lower() in buscar_grupo_por_id(c[5])[1].lower()]

    if not activos:
        print("No hay contactos que cumplan con el filtro.")
    else:
        print("\nID | NOMBRE                | TEL1        | TEL2        | CORREO                 | GRUPO")
        print("---------------------------------------------------------------------------------------------")
        for c in activos:
            gid = c[5]
            nombre_grupo = "(sin grupo)"
            
            g = buscar_grupo_por_id(gid)
            if g:
                nombre_grupo = g[1].strip()
            print(f"{str(c[0]).ljust(2)} | {c[1].strip().ljust(20)} | {c[2].strip().ljust(12)} | {c[3].strip().ljust(12)} | {c[4].strip().ljust(30)} | {nombre_grupo}")

    return activos

def eliminar_contacto():
    if not contactos_dict:
        print("No hay contactos para eliminar.")
        return

    print("\nContactos activos (id - nombre):")
    _listar_contactos_linea_base(False)

    cid = _ingresar_id_contacto()
    contacto = contactos_dict.get(cid)

    if not contacto or contacto[6]:
        print("No existe un contacto activo con ese ID.")
        return

    if input(f"¿Eliminar contacto '{contacto[1]}'? (s/n): ").strip().lower() == "s":
        contacto[6] = True
        print("Contacto marcado como eliminado (baja logica).")
    else:
        print("Operacion cancelada.")

def restaurar_contacto():
    anulados = [c for c in contactos_dict.values() if c[6]]
    if not anulados:
        print("No hay contactos anulados para restaurar.")
        return

    print("\nContactos anulados (id - nombre):")
    _listar_contactos_linea_base(True)

    cid = _ingresar_id_contacto()
    contacto = contactos_dict.get(cid)

    if not contacto or not contacto[6]:
        print("No existe un contacto anulado con ese ID.")
        return

    if input(f"¿Restaurar contacto '{contacto[1]}'? (s/n): ").strip().lower() == "s":
        contacto[6] = False
        print("Contacto restaurado.")
    else:
        print("Operacion cancelada.")

def editar_contacto():
    if not contactos_dict:
        print("No hay contactos para editar.")
        return

    print("\nContactos activos (id - nombre):")
    _listar_contactos_linea_base(False)

    cid = _ingresar_id_contacto()
    contacto = contactos_dict.get(cid)

    if not contacto or contacto[6]:
        print("No existe un contacto activo con ese ID.")
        return

    print("\nDeje vacio para mantener el valor actual.")

    campos = [
        (1, f"Nombre ({contacto[1]}): "),
        (2, f"Teléfono 1 ({contacto[2]}): "),
        (3, f"Teléfono 2 ({contacto[3]}): "),
        (4, f"Correo ({contacto[4]}): ")
    ]

    for i, msg in campos:
        nuevo_valor = input(msg).strip()
        if nuevo_valor != "":
            if i == 1 and nuevo_valor.replace(" ", "").isalpha():
                contacto[1] = nuevo_valor
            elif i in (2, 3) and nuevo_valor.isdigit():
                contacto[i] = nuevo_valor
            elif i == 4 and validar_correo(nuevo_valor):
                contacto[4] = nuevo_valor

    if input("¿Cambiar grupo? (s/n): ").strip().lower() == "s":
        contacto[5] = elegir_grupo()

    contactos_dict[cid] = contacto
    print("Contacto actualizado.")
