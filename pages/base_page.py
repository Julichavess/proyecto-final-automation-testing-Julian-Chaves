"""
Clase base para el patron Page Object Model.
Todas las paginas heredan de aca para reutilizar comportamientos comunes
(esperas explicitas, logging, etc.) en lugar de repetir codigo en cada Page.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger import get_logger

log = get_logger(__name__)


class BasePage:
    """Comportamiento comun a todas las paginas del sitio."""

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator):
        """Espera a que el elemento este presente y lo devuelve."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        """Espera a que haya al menos un elemento y devuelve la lista completa."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        """Espera a que el elemento sea clickeable y hace click."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type_text(self, locator, text: str):
        """Limpia el campo y escribe el texto indicado."""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def is_visible(self, locator) -> bool:
        """Devuelve True/False sin lanzar excepcion si el elemento no aparece."""
        try:
            return self.find(locator).is_displayed()
        except Exception:
            return False

    def get_text(self, locator) -> str:
        return self.find(locator).text
