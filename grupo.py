
grupos = []               # lista de listas: [id, nombre, anulado]
grupos_dict = {}          # diccionario auxiliar: {id: [id, nombre, anulado]}

#
next_id = lambda lista: 1 if len(lista) == 0 else max(fila[0] for fila in lista) + 1   

_buscar_grupo_index_por_id = lambda gid: next((i for i, g in enumerate(grupos) if g[0] == gid), -1)  # LAMBDA

_ingresar_id_grupo = lambda: int(input("Ingrese ID de grupo: ").strip()) \
    if (entrada := input("Ingrese ID de grupo: ").strip()).isdigit() else print("ID inválido. Debe ser numérico.")

buscar_grupo_por_id = lambda gid: grupos_dict.get(gid, None)   

existe_grupo_por_nombre = lambda nombre, ignorar_id=None: any(
    (not g[2]) and g[1].strip() == nombre.strip() and (ignorar_id is None or g[0] != ignorar_id)
    for g in grupos
)   

_hay_contactos_activos_en_grupo = lambda gid: any(
    (not c[6]) and (c[5] == gid) for c in __import__("contacto").contactos
)  


def listar_grupos():
    print("\nGrupos:")
    activos = list(filter(lambda g: not g[2], grupos))  
    if activos:
        for g in activos:
            print(str(g[0]).ljust(3) + " - " + g[1].strip().ljust(20))
    else:
        print("No hay grupos aun.")

def listar_grupos_inactivos():
    print("\nGrupos inactivos (baja lógica):")
    inactivos = list(filter(lambda g: g[2], grupos))  # LAMBDA en filter
    if inactivos:
        for g in inactivos:
            print(str(g[0]).ljust(3) + " - " + g[1].strip().ljust(20))
    else:
        print("(no hay grupos inactivos)")

# ==============================
# CRUD
# ==============================
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
    nuevo = [gid, nombre, False]
    grupos.append(nuevo)
    grupos_dict[gid] = nuevo   
    print("Grupo creado (id=" + str(gid) + ")")
    return gid

def eliminar_grupo():
    listar_grupos()
    if not grupos:
        print("No hay grupos para eliminar.")
        return

    gid = _ingresar_id_grupo()
    idx = _buscar_grupo_index_por_id(gid)
    if idx == -1 or grupos[idx][2]:
        print("No existe un grupo activo con ese ID.")
        return

    if _hay_contactos_activos_en_grupo(gid):
        print("✗ No se puede eliminar: hay contactos activos asignados a este grupo.")
        return

    nombre = grupos[idx][1]
    if input(f"¿Eliminar (baja lógica) grupo '{nombre}'? (s/n): ").strip().lower() == "s":
        grupos[idx][2] = True
        grupos_dict[gid][2] = True   
        print("Grupo marcado como eliminado (baja lógica).")
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
        print("No se puede restaurar: ya existe un grupo activo con ese nombre.")
        return

    if input(f"¿Restaurar grupo '{nombre}'? (s/n): ").strip().lower() == "s":
        grupos[idx][2] = False
        grupos_dict[gid][2] = False
        print("Grupo restaurado.")
    else:
        print("Operación cancelada.")

def editar_grupo():
    listar_grupos()
    if not grupos:
        print("No hay grupos para editar.")
        return

    gid = _ingresar_id_grupo()
    idx = _buscar_grupo_index_por_id(gid)
    if idx == -1 or grupos[idx][2]:
        print("No existe un grupo activo con ese ID.")
        return

    g = grupos[idx]
    actual_nom = g[1]
    nuevo_nombre = input(f"Nombre ({actual_nom}): ").strip()
    if nuevo_nombre != "":
        while (nuevo_nombre == "") or (not nuevo_nombre.replace(" ", "").isalpha()) or \
              (existe_grupo_por_nombre(nuevo_nombre, ignorar_id=g[0])):
            print("Nombre inválido o duplicado.")
            nuevo_nombre = input(f"Nombre ({actual_nom}): ").strip()
        g[1] = nuevo_nombre
        grupos_dict[gid][1] = nuevo_nombre

    grupos[idx] = g
    print("Grupo actualizado.")
