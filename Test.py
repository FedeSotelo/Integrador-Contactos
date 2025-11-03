from contacto import validar_correo
from grupo import grupos_dict, eliminar_grupo
from interacciones import _dias_en_mes

def test_validar_correo():
    assert validar_correo("persona@mail.com") == True
    assert validar_correo("") == True
    assert validar_correo("correo-malo") == False

def test_eliminar_grupo_inexistente():
    grupos_dict.clear()

    try:
        eliminar_grupo()
        assert False
    except LookupError:
        assert True

def test_dias_en_mes():
    # Meses normales
    assert _dias_en_mes(1, 2024) == 31    
    assert _dias_en_mes(9, 2024) == 30   
    # Febrero bisiesto
    assert _dias_en_mes(2, 2020) == 29
    # Febrero NO bisiesto
    assert _dias_en_mes(2, 2021) == 28
    # Mes inválido
    assert _dias_en_mes(13, 2024) == 0