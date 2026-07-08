"""
Fixtures compartidas de pytest para todo el proyecto:
  - driver: instancia limpia de Chrome por cada test
  - login_in_driver: driver ya logueado con usuario valido (para tests que
    no necesitan probar el login en si, sino algo posterior)
  - Hook de captura de screenshot automatica ante fallos, integrado al
    reporte HTML de pytest-html
"""

import json
import os
from datetime import datetime

import pytest
from selenium import webdriver

from pages.login_page import LoginPage
from utils.logger import get_logger

log = get_logger(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "login_data.json")


def _load_login_data() -> dict:
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="function")
def driver():
    """Instancia un Chrome nuevo (modo incognito) para cada test y lo cierra al final."""
    log.info("Iniciando driver de Chrome")
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    chrome_driver = webdriver.Chrome(options=options)
    chrome_driver.implicitly_wait(5)
    #chrome_driver.maximize_window()

    yield chrome_driver

    log.info("Cerrando driver de Chrome")
    chrome_driver.quit()


@pytest.fixture(scope="function")
def login_in_driver(driver):
    """
    Devuelve un driver ya logueado con el usuario valido definido en data/login_data.json.
    Pensada para tests que necesitan arrancar dentro de la app (inventario, carrito, etc.)
    sin repetir el flujo de login en cada uno.
    """
    data = _load_login_data()
    valid_user = data["valid_user"]

    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(valid_user["username"], valid_user["password"])

    return driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        test_driver = item.funcargs.get("driver")
        if test_driver:
            os.makedirs("screenshots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name
            screenshot_path = f"screenshots/{test_name}_{timestamp}.png"

            test_driver.save_screenshot(screenshot_path)
            log.error("Test '%s' fallo. Screenshot guardado en %s", test_name, screenshot_path)

            if hasattr(report, "extra"):
                import pytest_html
                html = (
                    f'<div><img src="../{screenshot_path}" alt="screenshot" '
                    f'style="width:304px;height:228px;" onclick="window.open(this.src)" '
                    f'align="right"/></div>'
                )
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
