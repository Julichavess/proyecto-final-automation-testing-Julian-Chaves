
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.logger import get_logger

log = get_logger(__name__)


def test_agregar_producto_al_carrito(login_in_driver):
    inventory_page = InventoryPage(login_in_driver)

    nombre_producto = inventory_page.get_first_product_name()
    inventory_page.add_first_product_to_cart()

    contador = inventory_page.get_cart_badge_count()
    assert contador == "1", "El producto no se agrego correctamente al carrito"

    inventory_page.go_to_cart()

    cart_page = CartPage(login_in_driver)
    item_en_carrito = cart_page.get_item_name()

    log.info("Producto agregado: '%s' | Producto en carrito: '%s'", nombre_producto, item_en_carrito)
    assert item_en_carrito == nombre_producto, "Los nombres de los productos no coinciden"
