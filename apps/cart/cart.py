from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:
    def __init__(self, request) -> None:
        """ Initialize cart object. """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # If non-existent, create new.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart

    def __iter__(self):
        """
        Iterate over products in the cart and retrieve them from the database.
        """
        product_ids = self.cart.keys()
        product

    def add(self, product: str, quantity=1, override_quantity=False):
        """
        Add a product to the cart or updates quantities.
        """
        product_id = str(product.id)

        # For new product addition.
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price)
            }

        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def remove(self, product):
        """ Removes a product from the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart["product_id"]
            self.save()

    def save(self):
        self.session.modified = True
