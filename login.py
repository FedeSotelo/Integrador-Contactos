import pwinput

def login():
    usuario_correcto = "Lionel Messi"
    password_correcto = "messi10"

    while True: 
        print("=== Login ===")
        usuario = input("Usuario: ").strip().lower()
        password = pwinput.pwinput("Contraseña: ", mask="*")

        if usuario == usuario_correcto.lower() and password == password_correcto:
            print("Bienvenido Lio 10")
            return True   
        else:
            print("Usuario o contraseña incorrectos. Intente de nuevo.\n")
