from pages.inventory_page import InventoryPage
from utils.logger import get_logger

log = get_logger(__name__)


def test_titulo_de_pagina_correcto(login_in_driver):
    inventory_page = InventoryPage(login_in_driver)
    assert inventory_page.get_page_title() == "Swag Labs", "El titulo de la pestaña no es correcto"


def test_hay_productos_visibles(login_in_driver):
    inventory_page = InventoryPage(login_in_driver)
    cantidad = inventory_page.get_products_count()
    log.info("Cantidad de productos encontrados: %s", cantidad)
    assert cantidad > 0, "No se encontraron productos en el inventario"


def test_elementos_de_ui_visibles(login_in_driver):
    inventory_page = InventoryPage(login_in_driver)
    assert inventory_page.is_menu_visible(), "No se encuentra el menu"
    assert inventory_page.is_sort_filter_visible(), "No se encuentra el filtro de orden"
