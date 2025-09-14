# {id: [id, nombre, anulado]}
grupos_dict = {}

next_id = lambda d: 1 if not d else max(d.keys()) + 1

buscar_grupo_por_id = lambda gid: grupos_dict.get(gid, None)

existe_grupo_por_nombre = lambda nombre, ignorar_id=None: any(
    (not g[2]) and g[1].strip().lower() == nombre.strip().lower() and (ignorar_id is None or g[0] != ignorar_id)
    for g in grupos_dict.values()
)

def _ingresar_id_grupo():
    entrada = input("Ingrese ID de grupo: ").strip()
    if entrada.isdigit():
        return int(entrada)
    print("ID inválido. Debe ser numérico.")
    return None


def listar_grupos():
    print("\nGrupos activos:")
    activos = [g for g in grupos_dict.values() if not g[2]]
    if activos:
        for g in activos:
            print(str(g[0]).ljust(3) + " - " + g[1].strip().ljust(20))
    else:
        print("(no hay grupos activos)")

def listar_grupos_inactivos():
    print("\nGrupos inactivos:")
    inactivos = [g for g in grupos_dict.values() if g[2]]
    if inactivos:
        for g in inactivos:
            print(str(g[0]).ljust(3) + " - " + g[1].strip().ljust(20))
    else:
        print("(no hay grupos inactivos)")


def crear_grupo_interactivo():
    print("\n=== Crear grupo ===")
    nombre = input("Nombre del nuevo grupo: ").strip()
    while nombre == "" or existe_grupo_por_nombre(nombre):
        if nombre == "":
            print("Nombre inválido (no puede estar vacío).")
        else:
            print("Nombre repetido en grupos activos.")
        nombre = input("Nombre del nuevo grupo: ").strip()

    gid = next_id(grupos_dict)
    nuevo = [gid, nombre, False]
    grupos_dict[gid] = nuevo
    print(f"Grupo creado (id={gid})")
    return gid


def eliminar_grupo():
    listar_grupos()
    if not grupos_dict:
        print("No hay grupos para eliminar.")
        return

    gid = _ingresar_id_grupo()
    if gid is None or gid not in grupos_dict or grupos_dict[gid][2]:
        print("No existe un grupo activo con ese ID.")
        return

    nombre = grupos_dict[gid][1]
    if input(f"¿Eliminar (baja logica) grupo '{nombre}'? (s/n): ").strip().lower() == "s":
        grupos_dict[gid][2] = True
        print("Grupo marcado como eliminado (baja logica).")
    else:
        print("Operacion cancelada.")


def restaurar_grupo():
    listar_grupos_inactivos()
    gid = _ingresar_id_grupo()
    if gid is None or gid not in grupos_dict or not grupos_dict[gid][2]:
        print("No existe un grupo inactivo con ese ID.")
        return

    nombre = grupos_dict[gid][1]
    if existe_grupo_por_nombre(nombre):
        print("No se puede restaurar: ya existe un grupo activo con ese nombre.")
        return

    if input(f"¿Restaurar grupo '{nombre}'? (s/n): ").strip().lower() == "s":
        grupos_dict[gid][2] = False
        print("Grupo restaurado.")
    else:
        print("Operacion cancelada.")


def editar_grupo():
    listar_grupos()
    if not grupos_dict:
        print("No hay grupos para editar.")
        return

    gid = _ingresar_id_grupo()
    if gid is None or gid not in grupos_dict or grupos_dict[gid][2]:
        print("No existe un grupo activo con ese ID.")
        return

    g = grupos_dict[gid]
    actual_nom = g[1]
    nuevo_nombre = input(f"Nombre ({actual_nom}): ").strip()
    if nuevo_nombre != "":
        while nuevo_nombre == "" or not nuevo_nombre.replace(" ", "").isalpha() or \
              existe_grupo_por_nombre(nuevo_nombre, ignorar_id=g[0]):
            print("Nombre inválido o duplicado.")
            nuevo_nombre = input(f"Nombre ({actual_nom}): ").strip()
        g[1] = nuevo_nombre

    grupos_dict[gid] = g
    print("Grupo actualizado.")
