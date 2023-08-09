from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe


def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''


order_payment.short_description = "Stripe payment"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_no", "first_name", "last_name", "email", "paid",
        order_payment, "updated", "created"
    ]
    list_filter = ["paid", "created", "updated"]
    inlines = [OrderItemInline]
