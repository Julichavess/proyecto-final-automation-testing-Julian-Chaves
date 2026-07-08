"""
Page Object de la pagina de login (https://www.saucedemo.com).
Concentra los locators y las acciones posibles sobre esta pagina especifica.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import get_logger

log = get_logger(__name__)


class LoginPage(BasePage):

    URL = "https://www.saucedemo.com/"

    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
        """Navega a la pagina de login."""
        log.info("Abriendo pagina de login: %s", self.URL)
        self.driver.get(self.URL)
        return self

    def login(self, username: str, password: str):
        """Completa usuario/clave y envia el formulario de login."""
        log.info("Intentando login con usuario '%s'", username)
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """Devuelve el texto de error mostrado tras un login invalido."""
        message = self.get_text(self.ERROR_MESSAGE)
        log.info("Mensaje de error obtenido: '%s'", message)
        return message
