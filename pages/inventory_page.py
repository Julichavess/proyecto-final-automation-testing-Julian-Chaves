"""
Page Object de la pagina de inventario (listado de productos) de saucedemo.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import get_logger

log = get_logger(__name__)


class InventoryPage(BasePage):

    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ADD_TO_CART_BUTTONS = (By.CLASS_NAME, "btn_inventory")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    BURGER_MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    SORT_FILTER = (By.CLASS_NAME, "product_sort_container")

    def get_page_title(self) -> str:
        return self.driver.title

    def get_products_count(self) -> int:
        return len(self.find_all(self.PRODUCT_ITEMS))

    def get_first_product_name(self) -> str:
        return self.get_text(self.PRODUCT_NAMES)

    def add_first_product_to_cart(self):
        log.info("Agregando el primer producto del listado al carrito")
        self.click(self.ADD_TO_CART_BUTTONS)

    def get_cart_badge_count(self) -> str:
        return self.get_text(self.CART_BADGE)

    def go_to_cart(self):
        log.info("Navegando al carrito")
        self.click(self.CART_LINK)

    def is_menu_visible(self) -> bool:
        return self.is_visible(self.BURGER_MENU_BUTTON)

    def is_sort_filter_visible(self) -> bool:
        return self.is_visible(self.SORT_FILTER)
