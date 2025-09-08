from contacto import contactos
from grupo import grupos
from interacciones import interacciones

def cantidad_contactos_por_grupo():
    print("\nCantidad de contactos por grupo:")
    for g in grupos:
        if not g[2]:  # grupo activo
            cant = len([c for c in contactos if c[5] == g[0] and not c[6]])
            print(f"- {g[1]}: {cant} contacto(s)")

def promedio_interacciones_por_contacto():
    total_contactos = len(contactos)
    total_interacciones = len(interacciones)
    promedio = total_interacciones / total_contactos if total_contactos > 0 else 0
    print(f"\nPromedio de interacciones por contacto: {promedio:.2f}")

def porcentaje_contactos_activos():
    total = len(contactos)
    activos = len([
        c for c in contactos
        if any(i[1] == c[0] for i in interacciones)
    ])
    porcentaje = (activos / total * 100) if total > 0 else 0
    print(f"\nPorcentaje de contactos activos: {porcentaje:.2f}%")