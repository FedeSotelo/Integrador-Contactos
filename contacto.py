import re
from grupo import grupos, listar_grupos, crear_grupo_interactivo, buscar_grupo_por_id, next_id

# [id, nombre, tel1, tel2, correo, idGrupo, anulado]
contactos = []
contactos_dict = {}   #  {id: [id, nombre, tel1, tel2, correo, idGrupo, anulado]}


validar_correo = lambda c: (c.strip() == "") or bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", c))


_buscar_contacto_index_por_id = lambda cid: next((i for i, c in enumerate(contactos) if c[0] == cid), -1)

def _ingresar_id_contacto():
    while True:
        entrada = input("Ingrese ID de contacto: ").strip()
        if entrada.isdigit():
            return int(entrada)
        print("ID inválido. Debe ser numérico.")

_listar_contactos_linea_base = lambda incluir_anulados=False: (
    print("\n".join([f"{str(c[0]).ljust(3)} - {c[1]}" for c in contactos if (not c[6]) or incluir_anulados]))
    if any((not c[6]) or incluir_anulados for c in contactos) else print("(no hay contactos a mostrar)")
)

def elegir_grupo():
    while True:
        listar_grupos()
        if len(grupos) == 0:
            print("No hay grupos, se creará uno.")
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
        print("Opción inválida.")


def alta_contacto():
    print("\n=== Alta de contacto ===")
    nombre = input("Nombre: ").strip()
    while nombre == "" or not nombre.replace(" ", "").isalpha():
        print("El nombre es obligatorio y debe contener solo letras.")
        nombre = input("Nombre (obligatorio): ").strip()

    tel1 = input("Telefono 1: ").strip()
    while tel1 == "" or not tel1.isdigit():
        print("El teléfono debe ser numérico y es obligatorio.")
        tel1 = input("Telefono 1 (obligatorio): ").strip()

    tel2 = input("Telefono 2 (opcional): ").strip()
    while tel2 != "" and not tel2.isdigit():
        print("El teléfono debe ser numérico o dejar vacío.")
        tel2 = input("Telefono 2 (opcional): ").strip()

    correo = input("Correo (opcional): ").strip()
    while not validar_correo(correo):
        print("Correo inválido.")
        correo = input("Correo (opcional): ").strip()

    id_grupo = elegir_grupo()

    cid = next_id(contactos)
    nuevo = [cid, nombre, tel1, tel2, correo, id_grupo, False]
    contactos.append(nuevo)
    contactos_dict[cid] = nuevo  
    print(f"Contacto creado (id={cid})")

def listar_contactos_detallado(filtro_nombre: str = "", filtro_grupo_desc: str = ""):
    activos = [c for c in contactos if not c[6]]  #aca solo se muestran los activos

    if filtro_nombre.strip() != "":
        activos = list(filter(lambda c: filtro_nombre.lower() in c[1].lower(), activos)) 

    if filtro_grupo_desc.strip() != "":
        activos = list(filter(
            lambda c: buscar_grupo_por_id(c[5]) and filtro_grupo_desc.lower() in buscar_grupo_por_id(c[5])[1].lower(),
            activos
        ))

    if len(activos) == 0:
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
            print(f"{str(c[0]).ljust(2)} | {c[1].strip().ljust(20)} | {c[2].strip().ljust(12)} | {c[3].strip().ljust(12)} | {c[4].strip().ljust(22)} | {nombre_grupo}")

    return activos

def eliminar_contacto():
    if len(contactos) == 0:
        print("No hay contactos para eliminar.")
        return

    print("\nContactos activos (id - nombre):")
    _listar_contactos_linea_base(incluir_anulados=False)

    cid = _ingresar_id_contacto()
    idx = _buscar_contacto_index_por_id(cid)
    if idx == -1 or contactos[idx][6]:
        print("No existe un contacto activo con ese ID.")
        return

    nombre = contactos[idx][1]
    if input(f"¿Eliminar contacto '{nombre}'? (s/n): ").strip().lower() == "s":
        contactos[idx][6] = True
        contactos_dict[cid][6] = True   
        print("Contacto marcado como eliminado (baja lógica).")
    else:
        print("Operación cancelada.")

def restaurar_contacto():
    anulados = [c for c in contactos if c[6]]
    if len(anulados) == 0:
        print("No hay contactos anulados para restaurar.")
        return

    print("\nContactos anulados (id - nombre):")
    _listar_contactos_linea_base(incluir_anulados=True)

    cid = _ingresar_id_contacto()
    idx = _buscar_contacto_index_por_id(cid)
    if idx == -1 or not contactos[idx][6]:
        print("No existe un contacto anulado con ese ID.")
        return

    if input(f"¿Restaurar contacto '{contactos[idx][1]}'? (s/n): ").strip().lower() == "s":
        contactos[idx][6] = False
        contactos_dict[cid][6] = False
        print("Contacto restaurado.")
    else:
        print("Operación cancelada.")

def editar_contacto():
    if len(contactos) == 0:
        print("No hay contactos para editar.")
        return

    print("\nContactos activos (id - nombre):")
    _listar_contactos_linea_base(incluir_anulados=False)

    cid = _ingresar_id_contacto()
    idx = _buscar_contacto_index_por_id(cid)
    if idx == -1 or contactos[idx][6]:
        print("No existe un contacto activo con ese ID.")
        return

    c = contactos[idx]
    print("\nDeje vacío para mantener el valor actual.")

    # usar tupla (campo, mensaje) para iterar validaciones
    campos = [
        (1, f"Nombre ({c[1]}): "),
        (2, f"Teléfono 1 ({c[2]}): "),
        (3, f"Teléfono 2 ({c[3]}): "),
        (4, f"Correo ({c[4]}): ")
    ]

    for i, msg in campos:
        nuevo_valor = input(msg).strip()
        if nuevo_valor != "":
            if i == 1 and nuevo_valor.replace(" ", "").isalpha():
                c[1] = nuevo_valor
            elif i in (2, 3) and nuevo_valor.isdigit():
                c[i] = nuevo_valor
            elif i == 4 and validar_correo(nuevo_valor):
                c[4] = nuevo_valor

    if input("¿Cambiar grupo? (s/n): ").strip().lower() == "s":
        id_grupo_nuevo = elegir_grupo()
        c[5] = id_grupo_nuevo

    contactos[idx] = c
    contactos_dict[cid] = c
    print("Contacto actualizado.")
