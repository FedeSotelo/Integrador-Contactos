from grupo import grupos, listar_grupos, crear_grupo_interactivo, buscar_grupo_por_id, next_id

# [id, nombre, tel1, tel2, correo, idGrupo, anulado]
contactos = []

def validar_correo(c):
    c = c.strip()
    if c == "":
        return True
    return ("@" in c) and ("." in c)

def _buscar_contacto_index_por_id(cid: int):
    i = 0
    while i < len(contactos):
        if contactos[i][0] == cid:
            return i
        i += 1
    return -1

def _ingresar_id_contacto():
    while True:
        entrada = input("Ingrese ID de contacto: ").strip()
        if entrada.isdigit():
            return int(entrada)
        print("ID inválido. Debe ser numérico.")

def _listar_contactos_linea_base(incluir_anulados=False):
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
        print("Correo invalido.")
        correo = input("Correo (opcional): ").strip()

    id_grupo = elegir_grupo()

    cid = next_id(contactos)
    contactos.append([cid, nombre, tel1, tel2, correo, id_grupo, False])  # anulado=False
    print("Contacto creado (id=" + str(cid) + ")")

def listar_contactos_detallado(filtro_nombre: str = "", filtro_grupo_desc: str = ""):
    activos = [c for c in contactos if not c[6]]  # solo activos

    # aplicar filtro por nombre
    if filtro_nombre.strip() != "":
        activos = [c for c in activos if filtro_nombre.lower() in c[1].lower()]

    # aplicar filtro por descripción de grupo
    if filtro_grupo_desc.strip() != "":
        activos_filtrados = []
        for c in activos:
            g = buscar_grupo_por_id(c[5])
            if g and filtro_grupo_desc.lower() in g[1].lower():
                activos_filtrados.append(c)
        activos = activos_filtrados

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
            id  = str(c[0]).ljust(2)
            nom = c[1].strip().ljust(20)
            t1  = c[2].strip().ljust(12)
            t2  = c[3].strip().ljust(12)
            cor = c[4].strip().ljust(22)
            print(id + " | " + nom + " | " + t1 + " | " + t2 + " | " + cor + " | " + nombre_grupo)

    return activos  # <-- DEVOLVÉ LA LISTA FILTRADA




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
    conf = input(f"¿Eliminar (baja logica) contacto '{nombre}'? (s/n): ").strip().lower()
    if conf == "s":
        contactos[idx][6] = True
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

    conf = input(f"¿Restaurar contacto '{contactos[idx][1]}'? (s/n): ").strip().lower()
    if conf == "s":
        contactos[idx][6] = False
        print("Contacto restaurado.")
    else:
        print("Operacion cancelada.")


def editar_contacto():
    if len(contactos) == 0:
        print("No hay contactos para editar.")
        return

    print("\nContactos activos (id - nombre):")

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

    c = contactos[idx]
    print("\nDeje vacio para mantener el valor actual.")


    actual_nom = c[1]
    nuevo_nombre = input(f"Nombre ({actual_nom}): ").strip()
    if nuevo_nombre != "":
        while (nuevo_nombre == "") or (not nuevo_nombre.replace(" ", "").isalpha()):
            print("El nombre debe contener solo letras (y espacios).")
            nuevo_nombre = input(f"Nombre ({actual_nom}): ").strip()
        c[1] = nuevo_nombre


    actual_t1 = c[2]
    nuevo_tel1 = input(f"Teléfono 1 ({actual_t1}): ").strip()
    if nuevo_tel1 != "":
        while (nuevo_tel1 == "") or (not (nuevo_tel1.isnumeric() or nuevo_tel1.isdigit())):
            print("El telefono debe ser numerico.")
            nuevo_tel1 = input(f"Teléfono 1 ({actual_t1}): ").strip()
        c[2] = nuevo_tel1

    actual_t2 = c[3] if c[3] else ""
    nuevo_tel2 = input(f"Telefono 2 ({actual_t2}): ").strip()
    if nuevo_tel2 != "":
        while not (nuevo_tel2.isnumeric() or nuevo_tel2.isdigit()):
            print("El teléfono debe ser numerico o deje vacío.")
            nuevo_tel2 = input(f"Teléfono 2 ({actual_t2}): ").strip()
        c[3] = nuevo_tel2

    actual_mail = c[4] if c[4] else ""
    nuevo_correo = input(f"Correo ({actual_mail}): ").strip()
    if nuevo_correo != "":
        while not (("@" in nuevo_correo) and ("." in nuevo_correo)):
            print("Correo invalido.")
            nuevo_correo = input(f"Correo ({actual_mail}): ").strip()
        c[4] = nuevo_correo

    resp = input("¿Cambiar grupo? (s/n): ").strip().lower()
    if resp == "s":
        id_grupo_nuevo = elegir_grupo()
        c[5] = id_grupo_nuevo

    contactos[idx] = c
    print("Contacto actualizado.")
