from contacto import contactos_dict, listar_contactos_detallado, obtener_nombre_y_tel, _ingresar_id_contacto
from grupo import buscar_grupo_por_id, listar_grupos, _ingresar_id_grupo
# Diccionario único: {id: [id, idContacto, descripcion, fecha, tipo, anulado]}
interacciones_dict = {}
tipos_interaccion = ["llamada", "mensaje", "email", "reunion", "videollamada", "otro"]

from functools import reduce

def next_id(d: dict) -> int:
    if not d:
        return 1
    return reduce(lambda a, b: a if a > b else b, d.keys()) + 1



# =====================================================
# Crear
# =====================================================
def elegir_contacto(filtroNombre: str = "", filtroGrupoDesc: str = ""):
    contactos_filtrados = listar_contactos_detallado(filtroNombre, filtroGrupoDesc)
    if len(contactos_filtrados) == 0:
        print("No hay contactos.")
        return None

    entrada = input("Ingrese id del contacto: ").strip()
    if entrada.isdigit():
        val = int(entrada)
        if val in contactos_dict and not contactos_dict[val][6]:  # existe y no está anulado
            return val
    print("ID inválido.")
    return None


def crear_interaccion():
    filtro_nombre = input("Filtrar por nombre (enter para todos): ").strip()
    filtro_grupo_desc = input("Filtrar por grupo (enter para todos): ").strip()
    idContacto = elegir_contacto(filtro_nombre, filtro_grupo_desc)
    if idContacto is None:
        return

    descripcion = input("Descripcion: ").strip()
    fecha = input("Fecha (DD/MM/AAAA): ").strip()
    while not _validar_fecha_completa(fecha):
        print("Fecha invalida. Ingresa una en formato valido (DD/MM/AAAA o DD-MM-AAAA).")
        fecha = input("Fecha (DD/MM/AAAA): ").strip()


    tipo = input(f"Tipo de interaccion ({', '.join(tipos_interaccion)}): ").strip().lower()
    while tipo not in tipos_interaccion:
        print("Tipo de interaccion no valido.")
        tipo = input(f"Tipo de interaccion ({', '.join(tipos_interaccion)}): ").strip().lower()

    iId = next_id(interacciones_dict)
    interacciones_dict[iId] = [iId, idContacto, descripcion, fecha, tipo, False]
    print("Interaccion creada con exito.")


def listar_interacciones(incluir_anuladas=False):
    print("\n=== Lista de interacciones ===")
    filas = [i for i in interacciones_dict.values() if (not i[5]) or incluir_anuladas]

    if not filas:
        print("(no hay interacciones)")
        return []

    print("ID | CONTACTO | DESCRIPCION | FECHA       | TIPO")
    print("----------------------------------------------------")
    for i in filas:
        c = contactos_dict.get(i[1])
        nombre = c[1] if c else "(desconocido)"
        print(f"{str(i[0]).ljust(2)} | {nombre.ljust(10)} | {i[2].ljust(12)} | {i[3].ljust(10)} | {i[4]}")
    return filas


def editar_interaccion():
    listar_interacciones()
    iid = int(input("ID de la interaccion a editar: ").strip())
    if iid not in interacciones_dict or interacciones_dict[iid][5]:
        print("No existe interaccion activa con ese ID.")
        return

    i = interacciones_dict[iid]
    nueva_desc = input(f"Descripcion ({i[2]}): ").strip()
    if nueva_desc != "":
        i[2] = nueva_desc

    nueva_fecha = input(f"Fecha ({i[3]}): ").strip()
    if nueva_fecha != "":
        i[3] = nueva_fecha

    nuevo_tipo = input(f"Tipo ({i[4]}): ").strip().lower()
    if nuevo_tipo != "" and nuevo_tipo in tipos_interaccion:
        i[4] = nuevo_tipo

    interacciones_dict[iid] = i
    print("Interaccion actualizada.")


def eliminar_interaccion():
    listar_interacciones()
    iid = int(input("ID de la interaccion a eliminar: ").strip())
    if iid not in interacciones_dict or interacciones_dict[iid][5]:
        print("No existe interaccion activa con ese ID.")
        return

    conf = input("¿Eliminar (baja logica)? (s/n): ").strip().lower()
    if conf == "s":
        interacciones_dict[iid][5] = True
        print("Interaccion eliminada (baja logica).")


def restaurar_interaccion():
    iid = int(input("ID de la interaccion a restaurar: ").strip())
    if iid in interacciones_dict and interacciones_dict[iid][5]:
        interacciones_dict[iid][5] = False
        print("Interaccion restaurada.")


def ver_historial_por_contacto():
    cid = _ingresar_id_contacto()  
    if cid not in contactos_dict or contactos_dict[cid][6]:
        print("No existe un contacto activo con ese ID.")
        return

    filas = [i for i in interacciones_dict.values() if i[1] == cid and not i[5]]
    if not filas:
        print("Ese contacto no tiene interacciones.")
        return

    info = obtener_nombre_y_tel(cid)
    if info:
        print(f"\nHistorial de interacciones de {info[0]} (tel: {info[1]}):")
    else:
        print(f"\nHistorial de interacciones del contacto {cid}:")

    for i in filas:
        print(f"- {i[3]}: {i[2]} ({i[4]})")


def ver_historial_por_grupo():
    print("\n=== Lista de grupos ===")
    listar_grupos()  

    gid = _ingresar_id_grupo()  
    if gid is None:
        print("ID de grupo invalido.")
        return

    contactos_en_grupo = [c[0] for c in contactos_dict.values() if c[5] == gid and not c[6]]
    filas = [i for i in interacciones_dict.values() if i[1] in contactos_en_grupo and not i[5]]

    if not filas:
        print("Ese grupo no tiene interacciones.")
        return

    g = buscar_grupo_por_id(gid)
    nombre_grupo = g[1] if g else "(desconocido)"
    print(f"\nHistorial de interacciones del grupo '{nombre_grupo}'")
    for i in filas:
        c = contactos_dict.get(i[1])
        nombre = c[1] if c else "(desconocido)"
        print(f"- {nombre} ({i[3]}): {i[2]} ({i[4]})")

def _es_bisiesto(anio: int) -> bool:
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

def _dias_en_mes(mes: int, anio: int) -> int:
    if mes in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif mes in [4, 6, 9, 11]:
        return 30
    elif mes == 2:
        return 29 if _es_bisiesto(anio) else 28
    else:
        return 0   # mes invalido
    
def _validar_fecha_completa(fecha: str) -> bool:
    if "/" in fecha:
        partes = fecha.split("/")
    elif "-" in fecha:
        partes = fecha.split("-")
    else:
        return False

    if len(partes) != 3:
        return False

    dia, mes, anio = partes
    if not (dia.isdigit() and mes.isdigit() and anio.isdigit()):
        return False

    dia, mes, anio = int(dia), int(mes), int(anio)

    if not (1 <= mes <= 12):
        return False

    max_dias = _dias_en_mes(mes, anio)
    if not (1 <= dia <= max_dias):
        return False

    return True

       