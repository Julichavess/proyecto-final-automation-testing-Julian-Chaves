import json
import os

import pytest

from pages.login_page import LoginPage
from utils.logger import get_logger

log = get_logger(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "login_data.json")

with open(DATA_PATH, encoding="utf-8") as f:
    _data = json.load(f)

VALID_USER = _data["valid_user"]
INVALID_LOGINS = _data["invalid_logins"]


def test_login_valido_redirige_a_inventario(driver):
    """Caso positivo: con credenciales validas, la app redirige a /inventory.html"""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(VALID_USER["username"], VALID_USER["password"])

    assert "/inventory.html" in driver.current_url, "No se redirigio a inventario"
    log.info("Login valido OK, redirigio correctamente a inventario")


@pytest.mark.parametrize(
    "caso",
    INVALID_LOGINS,
    ids=[c["case"] for c in INVALID_LOGINS],
)
def test_login_invalido_muestra_error(driver, caso):
    """Caso negativo parametrizado: distintas combinaciones de credenciales invalidas."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(caso["username"], caso["password"])

    mensaje_error = login_page.get_error_message()

    assert caso["expected_error"] in mensaje_error, (
        f"[{caso['case']}] Se esperaba el mensaje '{caso['expected_error']}' "
        f"pero se obtuvo '{mensaje_error}'"
    )
    assert "/inventory.html" not in driver.current_url, (
        f"[{caso['case']}] No deberia haber ingresado al inventario"
    )
