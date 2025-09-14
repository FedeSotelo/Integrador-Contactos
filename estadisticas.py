from contacto import contactos_dict
from grupo import grupos_dict
from interacciones import interacciones_dict, tipos_interaccion


def cantidad_contactos_por_grupo():
    print("\nCantidad de contactos por grupo:")
    for g in grupos_dict.values():
        if not g[2]:  # grupo activo
            cant = len([c for c in contactos_dict.values() if c[5] == g[0] and not c[6]])
            print(f"- {g[1]}: {cant} contacto(s)")


def promedio_interacciones_por_contacto():
    total_contactos = len([c for c in contactos_dict.values() if not c[6]])
    total_interacciones = len([i for i in interacciones_dict.values() if not i[5]])
    promedio = total_interacciones / total_contactos if total_contactos > 0 else 0
    print(f"\nPromedio de interacciones por contacto: {promedio:.2f}")


def porcentaje_contactos_activos():
    total = len([c for c in contactos_dict.values() if not c[6]])
    activos = len([
        c for c in contactos_dict.values() if not c[6] and
        any(i[1] == c[0] and not i[5] for i in interacciones_dict.values())
    ])
    porcentaje = (activos / total * 100) if total > 0 else 0
    print(f"\nPorcentaje de contactos activos: {porcentaje:.2f}%")


def contacto_con_mas_y_menos_interacciones():
    """
    Muestra el contacto con mayor y menor cantidad de interacciones.
    Si no hay interacciones registradas, lo indica por consola.
    """
    if not contactos_dict or not interacciones_dict:
        print("\nNo hay contactos o interacciones registradas.")
        return

    # Contar interacciones por contacto
    conteo = {c[0]: 0 for c in contactos_dict.values() if not c[6]}  # {idContacto: cantidad}
    for i in interacciones_dict.values():
        if not i[5]:  # solo interacciones activas
            if i[1] in conteo:
                conteo[i[1]] += 1

    if not conteo:
        print("\nNo hay contactos activos para mostrar estadísticas.")
        return

    # Buscar máximo y mínimo
    max_id = max(conteo, key=conteo.get)
    min_id = min(conteo, key=conteo.get)

    contacto_max = contactos_dict.get(max_id)
    contacto_min = contactos_dict.get(min_id)

    print("\nContacto con MAS interacciones:")
    print(f"- {contacto_max[1]} ({conteo[max_id]} interacciones)")

    print("\nContacto con MENOS interacciones:")
    print(f"- {contacto_min[1]} ({conteo[min_id]} interacciones)")


def matriz_contactos_por_grupo_y_tipo():
    """
    Muestra una matriz [grupos x tipos de interaccion] con la cantidad de interacciones.
    Filas = grupos, Columnas = tipos de interaccion.
    """
    if not grupos_dict or not interacciones_dict:
        print("\nNo hay datos suficientes para generar la matriz.")
        return

    columnas = tipos_interaccion
    matriz = []

    for g in grupos_dict.values():
        if not g[2]:  # grupo activo
            fila = [g[1]]  # arranca con el nombre del grupo
            for tipo in columnas:
                cant = len([
                    i for i in interacciones_dict.values()
                    if not i[5] and i[4] == tipo and
                       any(c[0] == i[1] and c[5] == g[0] and not c[6] for c in contactos_dict.values())
                ])
                fila.append(cant)
            matriz.append(fila)

    # Mostrar tabla
    print("\nInteracciones por grupo y tipo:")
    print("GRUPO".ljust(15) + " | " + " | ".join(c.ljust(12) for c in columnas))
    print("-" * (17 + len(columnas) * 15))
    for fila in matriz:
        print(fila[0].ljust(15) + " | " + " | ".join(str(x).ljust(12) for x in fila[1:]))
