from contacto import contactos, _buscar_contacto_index_por_id, listar_contactos_detallado
from grupo import crear_grupo_interactivo, buscar_grupo_por_id

interacciones = []  # lista de listas: [id, idContacto, descripcion, fecha, tipo, anulado]
interacciones_dict = {}  # diccionario: {id: datos}

tipos_interaccion = ["llamada", "mensaje", "email", "reunión", "videollamada", "otro"]


next_id = lambda lista: 1 if len(lista) == 0 else max(f[0] for f in lista) + 1

# =====================================================
# Crear
# =====================================================
def elegir_contacto(filtroNombre: str = "", filtroGrupoDesc: str = ""):
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


def crear_interaccion():
    filtro_nombre = input("Filtrar por nombre (enter para todos): ").strip()
    filtro_grupo_desc = input("Filtrar por grupo (enter para todos): ").strip()
    idContacto = elegir_contacto(filtro_nombre, filtro_grupo_desc)

    if idContacto is None:
        print("No se seleccionó ningún contacto.")
        return

    idx = _buscar_contacto_index_por_id(int(idContacto))
    if idx == -1:
        print("No existe un contacto con ese ID.")
        return

    descripcion = input("Descripción: ").strip()
    fecha = input("Fecha (DD/MM/AAAA): ").strip()

    tipo = input(f"Tipo de interacción ({', '.join(tipos_interaccion)}): ").strip().lower()
    while tipo not in tipos_interaccion:
        print("Tipo de interacción no válido.")
        tipo = input(f"Tipo de interacción ({', '.join(tipos_interaccion)}): ").strip().lower()

    iId = next_id(interacciones)
    nueva = [iId, idContacto, descripcion, fecha, tipo, False]
    interacciones.append(nueva)
    interacciones_dict[iId] = nueva
    print("✓ Interacción creada con éxito.")


def listar_interacciones(incluir_anuladas=False):
    print("\n=== Lista de interacciones ===")
    filas = [i for i in interacciones if (not i[5]) or incluir_anuladas]

    if not filas:
        print("(no hay interacciones)")
        return []

    print("ID | CONTACTO | DESCRIPCION | FECHA       | TIPO")
    print("----------------------------------------------------")
    for i in filas:
        c = contactos[_buscar_contacto_index_por_id(i[1])]
        print(f"{str(i[0]).ljust(2)} | {c[1].ljust(8)} | {i[2].ljust(12)} | {i[3].ljust(10)} | {i[4]}")
    return filas


def editar_interaccion():
    filas = listar_interacciones()
    if not filas:
        return

    try:
        iid = int(input("ID de la interacción a editar: ").strip())
    except:
        print("ID inválido.")
        return

    if iid not in interacciones_dict or interacciones_dict[iid][5]:
        print("No existe interacción activa con ese ID.")
        return

    i = interacciones_dict[iid]
    print("\nDeje vacío para mantener el valor actual.")

    nueva_desc = input(f"Descripción ({i[2]}): ").strip()
    if nueva_desc != "":
        i[2] = nueva_desc

    nueva_fecha = input(f"Fecha ({i[3]}): ").strip()
    if nueva_fecha != "":
        i[3] = nueva_fecha

    nuevo_tipo = input(f"Tipo ({i[4]}): ").strip().lower()
    if nuevo_tipo != "" and nuevo_tipo in tipos_interaccion:
        i[4] = nuevo_tipo

    interacciones_dict[iid] = i
    print("✓ Interacción actualizada.")


def eliminar_interaccion():
    filas = listar_interacciones()
    if not filas:
        return

    try:
        iid = int(input("ID de la interacción a eliminar: ").strip())
    except:
        print("ID inválido.")
        return

    if iid not in interacciones_dict or interacciones_dict[iid][5]:
        print("No existe interacción activa con ese ID.")
        return

    conf = input("¿Eliminar (baja lógica)? (s/n): ").strip().lower()
    if conf == "s":
        interacciones_dict[iid][5] = True
        print("✓ Interacción eliminada (baja lógica).")
    else:
        print("Operación cancelada.")


def restaurar_interaccion():
    anuladas = [i for i in interacciones if i[5]]
    if not anuladas:
        print("No hay interacciones anuladas.")
        return

    try:
        iid = int(input("ID de la interacción a restaurar: ").strip())
    except:
        print("ID inválido.")
        return

    if iid in interacciones_dict and interacciones_dict[iid][5]:
        interacciones_dict[iid][5] = False
        print("✓ Interacción restaurada.")
    else:
        print("No existe interacción anulada con ese ID.")

# Historiales

def ver_historial_por_contacto():
    try:
        cid = int(input("ID de contacto: ").strip())
    except:
        print("ID inválido.")
        return

    filas = [i for i in interacciones if i[1] == cid and not i[5]]
    if not filas:
        print("Ese contacto no tiene interacciones.")
        return

    print(f"\nHistorial de interacciones del contacto {cid}:")
    for i in filas:
        print(f"- {i[3]}: {i[2]} ({i[4]})")


def ver_historial_por_grupo():
    try:
        gid = int(input("ID de grupo: ").strip())
    except:
        print("ID inválido.")
        return

    # contactos en el grupo
    contactos_en_grupo = [c[0] for c in contactos if c[5] == gid and not c[6]]

    filas = [i for i in interacciones if i[1] in contactos_en_grupo and not i[5]]
    if not filas:
        print("Ese grupo no tiene interacciones.")
        return

    g = buscar_grupo_por_id(gid)
    print(f"\nHistorial de interacciones del grupo '{g[1]}'")
    for i in filas:
        c = contactos[_buscar_contacto_index_por_id(i[1])]
        print(f"- {c[1]} ({i[3]}): {i[2]} ({i[4]})")

