grupos = []  # [id, afinidad]

def next_id(lista):
    if len(lista) == 0:
        return 1
    ids = [fila[0] for fila in lista]
    return max(ids) + 1

def listar_grupos():
    if len(grupos) == 0:
        print("No hay grupos aun.")
    else:
        print("\nGrupos:")
        for g in grupos:
            print(str(g[0]) + " - " + g[1])

def existe_grupo_por_nombre(nombre):
    for g in grupos:
        if g[1] == nombre:
            return True
    return False

def crear_grupo_interactivo():
    print("\n=== Crear grupo ===")
    nombre = input("Nombre del nuevo grupo: ")
    while nombre == "" or existe_grupo_por_nombre(nombre):
        print("Nombre invalido o repetido.")
        nombre = input("Nombre del nuevo grupo: ")
    gid = next_id(grupos)
    grupos.append([gid, nombre])
    print("Grupo creado (id=" + str(gid) + ")")
    return gid

def buscar_grupo_por_id(idg):
    for g in grupos:
        if g[0] == idg:
            return g
    return None
