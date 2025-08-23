from grupo import grupos, listar_grupos, crear_grupo_interactivo, buscar_grupo_por_id, next_id

contactos = []  # [id, nombre, tel1, tel2, correo, idGrupo]

def validar_correo(c):
    if c == "":
        return True
    return ("@" in c) and ("." in c)

def elegir_grupo():
    while True:
        listar_grupos()
        if len(grupos) == 0:
            print("No hay grupos, se creara uno.")
            return crear_grupo_interactivo()

        print("0: Crear grupo nuevo")
        entrada = input("Ingrese id de grupo (o 0): ")
        es_numero = True
        if entrada == "":
            es_numero = False
        else:
            for caracter in entrada:
                if caracter not in "0123456789":
                    es_numero = False
                    break
        if es_numero:
            val = int(entrada)
            if val == 0:
                return crear_grupo_interactivo()
            g = buscar_grupo_por_id(val)
            if g is not None:
                return val
        print("Opción inválida.")

def alta_contacto():
    print("\n=== Alta de contacto ===")
    nombre = input("Nombre: ")
    while nombre == "":
        nombre = input("Nombre (obligatorio): ")

    tel1 = input("Telefono 1: ")
    while tel1 == "":
        tel1 = input("Telefono 1 (obligatorio): ")

    tel2 = input("Telefono 2 (opcional): ")
    correo = input("Correo (opcional): ")
    while not validar_correo(correo):
        print("Correo inválido.")
        correo = input("Correo (opcional): ")

    id_grupo = elegir_grupo()

    cid = next_id(contactos)
    contactos.append([cid, nombre, tel1, tel2, correo, id_grupo])
    print("Contacto creado (id=" + str(cid) + ")")

def listar_contactos_detallado():
    if len(contactos) == 0:
        print("No hay contactos cargados.")
        return
    print("\nID | NOMBRE                | TEL1        | TEL2        | CORREO                 | GRUPO")
    print("---------------------------------------------------------------------------------------------")
    for c in contactos:
        gid = c[5]
        nombre_grupo = "(sin grupo)"
        g = buscar_grupo_por_id(gid)
        if g:
            nombre_grupo = g[1]
        id  = str(c[0])
        nom = c[1].ljust(20)
        tel1  = c[2].ljust(12)
        tel2  = c[3].ljust(12)
        correo = c[4].ljust(22)
        print(id + " | " + nom + " | " + tel1 + " | " + tel2 + " | " + correo + " | " + nombre_grupo)
