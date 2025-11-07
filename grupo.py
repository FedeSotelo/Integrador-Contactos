
from archivo import agregar_datosGrupo;
from archivo import RUTA_ARCHIVO_GRUPO,listar_grupos,eliminar_grupo,restaurar_grupo,editar_grupo, buscar_grupo_por_id, listar_grupos_inactivos
import json, os

def next_id() -> int:
    if not os.path.exists(RUTA_ARCHIVO_GRUPO):
        return 1
    with open(RUTA_ARCHIVO_GRUPO, "r", encoding="UTF-8") as arch:
        try:
            grupos = json.load(arch)
        except json.JSONDecodeError:
            return 1
        if not grupos:
            return 1
        return max(g["id"] for g in grupos) + 1


def existe_grupo_por_nombre(nombre: str, ignorar_id=None) -> bool:
    """
    Devuelve True si ya existe un grupo activo con ese nombre.
    Lee directamente desde grupo.json y evita duplicados.
    """
    if not os.path.exists(RUTA_ARCHIVO_GRUPO) or os.path.getsize(RUTA_ARCHIVO_GRUPO) == 0:
        return False

    with open(RUTA_ARCHIVO_GRUPO, "r", encoding="UTF-8") as archivo:
        grupos = json.load(archivo)
        for g in grupos:
            mismo_nombre = g["nombre"].strip().lower() == nombre.strip().lower()
            activo = g.get("anulado", False) is False  # solo grupos activos
            distinto_id = (ignorar_id is None or g["id"] != ignorar_id)

            if mismo_nombre and activo and distinto_id:
                return True
    return False

def _ingresar_id_grupo():
    entrada = input("Ingrese ID de grupo: ").strip()
    if entrada.isdigit():
        return int(entrada)
    print("ID inválido. Debe ser numérico.")
    return None


def mostrar_grupos():
    listar_grupos()


def crear_grupo_interactivo():
    print("\n=== Crear grupo ===")
    nombre = input("Nombre del nuevo grupo: ").strip()

    while nombre == "" or existe_grupo_por_nombre(nombre):
        if nombre == "":
            print("El nombre no puede estar vacío.")
        else:
            print("Ya existe un grupo activo con ese nombre.")
        nombre = input("Nombre del nuevo grupo: ").strip()

    gid = next_id()

    nuevo_grupo = {
        "id": gid,
        "nombre": nombre,
        "anulado": False
    }

    agregar_datosGrupo(nuevo_grupo)
    print(f"Grupo creado con éxito (ID={gid})")

    return gid

def baja_grupo():
    listar_grupos()
    eliminar_grupo()


def reactivar_grupo():
    listar_grupos_inactivos()
    restaurar_grupo()

def editar_grupo_archivo():
  
    print("\n=== Editar grupo ===")
    editar_grupo()  