from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):

    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def get_item_name(self) -> str:
        return self.get_text(self.ITEM_NAME)

    def go_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
