import pytest
from contacto import validar_correo
from grupo import grupos_dict, eliminar_grupo
from interacciones import _dias_en_mes

@pytest.mark.parametrize(
    "correo, esperado",
    [
        ("persona@mail.com", True),   # correo válido
        ("", True),                   # vacío permitido por tu función
        ("correo-malo", False),       # sin @ → inválido
    ]
)
def test_validar_correo(correo, esperado):
    assert validar_correo(correo) == esperado

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