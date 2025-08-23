
grupos = []  # lista de listas

def next_id(lista):
    if len(lista) == 0:
        return 1
    ids = [fila[0] for fila in lista]
    return max(ids) + 1

def _buscar_grupo_index_por_id(gid):
    i = 0
    while i < len(grupos):
        if grupos[i][0] == gid:
            return i
        i += 1
    return -1

def _ingresar_id_grupo():
    while True:
        entrada = input("Ingrese ID de grupo: ").strip()
        if entrada.isdigit():
            return int(entrada)
        print("ID inválido. Debe ser numérico.")

def buscar_grupo_por_id(idg):
    i = 0
    while i < len(grupos):
        if grupos[i][0] == idg:
            return grupos[i]
        i += 1
    return None

def existe_grupo_por_nombre(nombre, ignorar_id=None):
    nombre_norm = nombre.strip()
    i = 0
    while i < len(grupos):
        g = grupos[i]
        if (ignorar_id is None or g[0] != ignorar_id):
            if (not g[2]) and (g[1].strip() == nombre_norm):
                return True
        i += 1
    return False

def _hay_contactos_activos_en_grupo(gid):
    from contacto import contactos  
    i = 0
    while i < len(contactos):
        c = contactos[i]
        if (not c[6]) and (c[5] == gid):
            return True
        i += 1
    return False

def listar_grupos():
    hay = False
    print("\nGrupos:")
    i = 0
    while i < len(grupos):
        g = grupos[i]
        if not g[2]:
            print(str(g[0]).ljust(3) + " - " + g[1].strip().ljust(20))
            hay = True
        i += 1
    if not hay:
        print("No hay grupos aun.")

def listar_grupos_inactivos():
    hay = False
    print("\nGrupos inactivos (baja lógica):")
    i = 0
    while i < len(grupos):
        g = grupos[i]
        if g[2]:
            print(str(g[0]).ljust(3) + " - " + g[1].strip().ljust(20))
            hay = True
        i += 1
    if not hay:
        print("(no hay grupos inactivos)")

def crear_grupo_interactivo():
    print("\n=== Crear grupo ===")
    nombre = input("Nombre del nuevo grupo: ").strip()
    while (nombre == "") or existe_grupo_por_nombre(nombre):
        if nombre == "":
            print("Nombre inválido (no puede estar vacío).")
        else:
            print("Nombre repetido en grupos activos.")
        nombre = input("Nombre del nuevo grupo: ").strip()

    gid = next_id(grupos)
    grupos.append([gid, nombre, False])  # anulado=False
    print("Grupo creado (id=" + str(gid) + ")")
    return gid

def eliminar_grupo():
    hay = False
    print("\nGrupos (activos):")
    i = 0
    while i < len(grupos):
        g = grupos[i]
        if not g[2]:
            print(f"{str(g[0]).ljust(3)} - {g[1]}")
            hay = True
        i += 1
    if not hay:
        print("No hay grupos para eliminar.")
        return

    gid = _ingresar_id_grupo()
    idx = _buscar_grupo_index_por_id(gid)
    if idx == -1 or grupos[idx][2]:
        print("No existe un grupo activo con ese ID.")
        return

    if _hay_contactos_activos_en_grupo(gid):
        print("✗ No se puede eliminar: hay contactos activos asignados a este grupo.")
        print("Sugerencia: reasigne esos contactos a otro grupo y vuelva a intentar.")
        return

    nombre = grupos[idx][1]
    conf = input(f"¿Eliminar (baja lógica) grupo '{nombre}'? (s/n): ").strip().lower()
    if conf == "s":
        grupos[idx][2] = True 
        print("✓ Grupo marcado como eliminado (baja lógica).")
    else:
        print("Operación cancelada.")

def restaurar_grupo():
    listar_grupos_inactivos()
    gid = _ingresar_id_grupo()
    idx = _buscar_grupo_index_por_id(gid)
    if idx == -1 or (not grupos[idx][2]):
        print("No existe un grupo inactivo con ese ID.")
        return

    nombre = grupos[idx][1]
    if existe_grupo_por_nombre(nombre):
        print("✗ No se puede restaurar: ya existe un grupo activo con ese nombre.")
        return

    conf = input(f"¿Restaurar grupo '{nombre}'? (s/n): ").strip().lower()
    if conf == "s":
        grupos[idx][2] = False
        print("✓ Grupo restaurado.")
    else:
        print("Operación cancelada.")

def editar_grupo():
    hay = False
    print("\nGrupos (activos):")
    i = 0
    while i < len(grupos):
        g = grupos[i]
        if not g[2]:
            print(f"{str(g[0]).ljust(3)} - {g[1]}")
            hay = True
        i += 1
    if not hay:
        print("No hay grupos para editar.")
        return

    gid = _ingresar_id_grupo()
    idx = _buscar_grupo_index_por_id(gid)
    if idx == -1 or grupos[idx][2]:
        print("No existe un grupo activo con ese ID.")
        return

    g = grupos[idx]
    actual_nom = g[1]
    print("\nDeje vacío para mantener el valor actual.")

    nuevo_nombre = input(f"Nombre ({actual_nom}): ").strip()
    if nuevo_nombre != "":
        while (nuevo_nombre == "") or (not nuevo_nombre.replace(" ", "").isalpha()) or \
              (existe_grupo_por_nombre(nuevo_nombre, ignorar_id=g[0])):
            if nuevo_nombre == "":
                print("El nombre no puede estar vacío.")
            elif not nuevo_nombre.replace(" ", "").isalpha():
                print("El nombre debe contener solo letras.")
            else:
                print("Ya existe un grupo activo con ese nombre.")
            nuevo_nombre = input(f"Nombre ({actual_nom}): ").strip()
        g[1] = nuevo_nombre

    grupos[idx] = g
    print("Grupo actualizado.")
