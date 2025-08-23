# contacto.py

from grupo import grupos, listar_grupos, crear_grupo_interactivo, buscar_grupo_por_id, next_id

# Cada contacto: [id, nombre, tel1, tel2, correo, idGrupo, anulado]
contactos = []

def validar_correo(c):
    c = c.strip()
    if c == "":
        return True
    return ("@" in c) and ("." in c)

def _buscar_contacto_index_por_id(cid: int) -> int:
    """Devuelve el índice del contacto con id=cid o -1 si no existe."""
    i = 0
    while i < len(contactos):
        if contactos[i][0] == cid:
            return i
        i += 1
    return -1

def _ingresar_id_contacto() -> int:
    """Pide un ID numérico usando strip()+isdigit()."""
    while True:
        entrada = input("Ingrese ID de contacto: ").strip()
        if entrada.isdigit():
            return int(entrada)
        print("ID inválido. Debe ser numérico.")

def _listar_contactos_linea_base(incluir_anulados=False):
    """Muestra id - nombre (filtra anulados salvo que se indique lo contrario)."""
    hay = False
    for c in contactos:
        if (not c[6]) or incluir_anulados:
            print(f"{str(c[0]).ljust(3)} - {c[1]}")
            hay = True
    if not hay:
        print("(no hay contactos a mostrar)")

def elegir_grupo():
    while True:
        listar_grupos()
        if len(grupos) == 0:
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
        print("Opción inválida.")

def alta_contacto():
    print("\n=== Alta de contacto ===")
    nombre = input("Nombre: ").strip()
    while nombre == "" or not nombre.replace(" ", "").isalpha():
        print("El nombre es obligatorio y debe contener solo letras.")
        nombre = input("Nombre (obligatorio): ").strip()

    tel1 = input("Telefono 1: ").strip()
    while tel1 == "" or not tel1.isnumeric():
        print("El teléfono debe ser numérico y es obligatorio.")
        tel1 = input("Telefono 1 (obligatorio): ").strip()

    tel2 = input("Telefono 2 (opcional): ").strip()
    while tel2 != "" and not tel2.isnumeric():
        print("El teléfono debe ser numérico o dejar vacío.")
        tel2 = input("Telefono 2 (opcional): ").strip()

    correo = input("Correo (opcional): ").strip()
    while not validar_correo(correo):
        print("Correo inválido.")
        correo = input("Correo (opcional): ").strip()

    id_grupo = elegir_grupo()

    cid = next_id(contactos)
    contactos.append([cid, nombre, tel1, tel2, correo, id_grupo, False])  # anulado=False
    print("✓ Contacto creado (id=" + str(cid) + ")")

def listar_contactos_detallado():
    activos = [c for c in contactos if not c[6]]
    if len(activos) == 0:
        print("No hay contactos cargados.")
        return

    print("\nID | NOMBRE                | TEL1        | TEL2        | CORREO                 | GRUPO")
    print("---------------------------------------------------------------------------------------------")
    for c in contactos:
        if c[6]:  # anulado=True → no mostrar
            continue
        gid = c[5]
        nombre_grupo = "(sin grupo)"
        g = buscar_grupo_por_id(gid)
        if g:
            nombre_grupo = g[1].strip()
        id_txt  = str(c[0]).ljust(2)
        nom     = c[1].strip().ljust(20)
        t1      = c[2].strip().ljust(12)
        t2      = c[3].strip().ljust(12)
        cor     = c[4].strip().ljust(22)
        print(id_txt + " | " + nom + " | " + t1 + " | " + t2 + " | " + cor + " | " + nombre_grupo)

def eliminar_contacto():
    # Baja lógica: anulado=True
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
    conf = input(f"¿Eliminar (baja lógica) contacto '{nombre}'? (s/n): ").strip().lower()
    if conf == "s":
        contactos[idx][6] = True
        print("✓ Contacto marcado como eliminado (baja lógica).")
    else:
        print("Operación cancelada.")

# (Opcional) restaurar contacto anulado
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

    conf = input(f"¿Restaurar contacto '{contactos[idx][1]}'? (s/n): ").strip().lower()
    if conf == "s":
        contactos[idx][6] = False
        print("✓ Contacto restaurado.")
    else:
        print("Operación cancelada.")


def editar_contacto():
    if len(contactos) == 0:
        print("No hay contactos para editar.")
        return

    print("\nContactos activos (id - nombre):")
    # listamos solo activos
    hay = False
    for c in contactos:
        if not c[6]:
            print(f"{str(c[0]).ljust(3)} - {c[1]}")
            hay = True
    if not hay:
        print("(no hay contactos activos)")
        return

    cid = _ingresar_id_contacto()
    idx = _buscar_contacto_index_por_id(cid)
    if idx == -1 or contactos[idx][6]:
        print("No existe un contacto activo con ese ID.")
        return

    # c = [id, nombre, tel1, tel2, correo, idGrupo, anulado]
    c = contactos[idx]
    print("\nDeje vacío para mantener el valor actual.")

    # nombre
    actual_nom = c[1]
    nuevo_nombre = input(f"Nombre ({actual_nom}): ").strip()
    if nuevo_nombre != "":
        while (nuevo_nombre == "") or (not nuevo_nombre.replace(" ", "").isalpha()):
            print("El nombre debe contener solo letras (y espacios).")
            nuevo_nombre = input(f"Nombre ({actual_nom}): ").strip()
        c[1] = nuevo_nombre

    # tel1
    actual_t1 = c[2]
    nuevo_tel1 = input(f"Teléfono 1 ({actual_t1}): ").strip()
    if nuevo_tel1 != "":
        while (nuevo_tel1 == "") or (not (nuevo_tel1.isnumeric() or nuevo_tel1.isdigit())):
            print("El telefono debe ser numerico.")
            nuevo_tel1 = input(f"Teléfono 1 ({actual_t1}): ").strip()
        c[2] = nuevo_tel1

    # tel2 (opcional)
    actual_t2 = c[3] if c[3] else ""
    nuevo_tel2 = input(f"Telefono 2 ({actual_t2}): ").strip()
    if nuevo_tel2 != "":
        while not (nuevo_tel2.isnumeric() or nuevo_tel2.isdigit()):
            print("El teléfono debe ser numerico o deje vacío.")
            nuevo_tel2 = input(f"Teléfono 2 ({actual_t2}): ").strip()
        c[3] = nuevo_tel2

    # correo (opcional)
    actual_mail = c[4] if c[4] else ""
    nuevo_correo = input(f"Correo ({actual_mail}): ").strip()
    if nuevo_correo != "":
        while not (("@" in nuevo_correo) and ("." in nuevo_correo)):
            print("Correo inválido.")
            nuevo_correo = input(f"Correo ({actual_mail}): ").strip()
        c[4] = nuevo_correo

    resp = input("¿Cambiar grupo? (s/n): ").strip().lower()
    if resp == "s":
        id_grupo_nuevo = elegir_grupo()
        c[5] = id_grupo_nuevo

    contactos[idx] = c
    print("Contacto actualizado.")
