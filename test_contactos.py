import pytest
from contacto import validar_correo
from interacciones import _dias_en_mes
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


def test_dias_en_mes():
    assert _dias_en_mes(1, 2024) == 31    
    assert _dias_en_mes(9, 2024) == 30   
    assert _dias_en_mes(2, 2020) == 29
    assert _dias_en_mes(2, 2021) == 28
    assert _dias_en_mes(13, 2024) == 0



def test_calculo_promedio_interacciones(tmp_path):
    ruta_falsa = tmp_path / "interacciones.json"
    interacciones = [
        {"id": 1, "id_contacto": 1, "descripcion": "test", "fecha": "2025-11-04", "tipo": "llamada", "anulado": False}
    ]
    with open(ruta_falsa, "w", encoding="UTF-8") as f:
        json.dump(interacciones, f)

    original = RUTA_ARCHIVO_INTERACCIONES
    try:
        import estadisticas
        estadisticas.RUTA_ARCHIVO_INTERACCIONES = str(ruta_falsa)
        promedio_interacciones_por_contacto()
    finally:
        estadisticas.RUTA_ARCHIVO_INTERACCIONES = original