import pytest
from contacto import validar_correo
from interacciones import _dias_en_mes
from archivo import _ingresar_id_contacto  
import json
import os
from estadisticas import promedio_interacciones_por_contacto, RUTA_ARCHIVO_INTERACCIONES
@pytest.mark.parametrize(
    "correo, esperado",
    [
        ("persona@mail.com", True),   
        ("", True),                   
        ("correo-malo", False),       
    ]
)
def test_validar_correo_falla(correo, esperado):
    assert validar_correo(correo) == esperado

@pytest.mark.parametrize(
    "mes, anio, esperado",
    [
        (1, 2024, 31),
        (9, 2024, 30),
        (2, 2020, 29),
        (2, 2021, 28),
        (13, 2024, 0),
    ]
)
def test_dias_en_mes(mes, anio, esperado):
    assert _dias_en_mes(mes, anio) == esperado



@pytest.mark.parametrize(
    "entradas, esperado",
    [
        (["5"], 5),
        (["abc", "10"], 10),
        (["", "7"], 7),
    ]
)
def test_ingresar_id_contacto(monkeypatch, capsys, entradas, esperado):
    # Simula entradas consecutivas del usuario
    monkeypatch.setattr("builtins.input", lambda _: entradas.pop(0))

    resultado = _ingresar_id_contacto()

    salida = capsys.readouterr().out

    assert resultado == esperado

    # Si hubo una entrada inválida, muestra el mensaje de error
    if esperado != int(entradas[-1]) if entradas else False:
        assert "ID inválido" in salida or salida == ""