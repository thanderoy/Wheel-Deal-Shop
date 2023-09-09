from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.coupons.models import Coupon
from apps.shop.models import Product

from .utils import generate_order_no


class Order(BaseModel):
    order_no = models.CharField(
        max_length=5, unique=True, default=generate_order_no
    )
    stripe_id = models.CharField(max_length=250, blank=True)
    first_name = models.CharField(_("first_name"), max_length=50)
    last_name = models.CharField(_("last_name"), max_length=50)
    email = models.EmailField(_("email"),)
    address = models.CharField(_("address"), max_length=250)
    postal_code = models.CharField(_("postal_code"), max_length=20)
    city = models.CharField(_("city"), max_length=100)
    paid = models.BooleanField(default=False)

    # Coupon Related - discount is preserved even if Coupon object is deleted.
    coupon = models.ForeignKey(
        Coupon, related_name="orders", null=True, blank=True,
        on_delete=models.SET_NULL
    )
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self) -> str:
        return f"Order {self.id}"

    def get_total_cost_before_discount(self) -> int:
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self) -> int:
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost(self) -> int:
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    def get_stripe_url(self):
        if not self.stripe_id:
            return ""
        if '_test_' in settings.STRIPE_SECRET_KEY:
            path = '/test/'
        else:
            path = '/'
        return f"https://dashboard.stripe.com{path}payments/{self.stripe_id}"


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return str(self.id)

    def get_cost(self) -> int:
        return self.price * self.quantity
