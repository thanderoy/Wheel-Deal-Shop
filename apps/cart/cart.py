from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:
    """
    Cart objects are session based. Objects should be simple enough for
        serialization. Data for each product includes:
            * ID - UUID string.
            * Quantity - Integer.
            * Unit Price - 2 Place Decimal.
    Product prices are stored as when the time objects was added to cart. Any
        future price changes do not affects items in the cart.
    """

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
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products.iterator():
            cart[str(product.id)]["product"] = product
        for item in iter(cart.values()):
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def save(self) -> None:
        self.session.modified = True

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

    def remove(self, product) -> None:
        """ Removes a product from the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart["product_id"]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )
