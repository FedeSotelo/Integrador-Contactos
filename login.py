import pwinput

def login():
    usuarios = {
        "lionel messi": "messi10",
        "cristiano ronaldo": "cr7siuu"
    }

    while True:
        print("=== Login ===")
        usuario = input("Usuario: ").strip().lower()
        password = pwinput.pwinput("Contraseña: ", mask="*")

        if usuario in usuarios and password == usuarios[usuario]:
            print(f"Bienvenido {usuario.title()}!")
            return True
        else:
            print("Usuario o contraseña incorrectos. Intente de nuevo.\n")
