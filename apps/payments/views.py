from decimal import Decimal

import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.orders.models import Order

# Create Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order_no = request.session.get('order_no', None)
    order = get_object_or_404(Order, order_no=order_no)

    if request.method == "POST":
        success_url = request.build_absolute_uri(reverse("payment:completed"))
        cancel_url = request.build_absolute_uri(reverse("payment:canceled"))

        # Stripe checkout session data
        session_data = {
            "mode": "payment",
            "client_reference_id": order.order_no,
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": []
        }

        # Add order items
        for item in order.items.all().iterator():
            session_data.get("line_items").append({
                "price_data": {
                    "unit_amount": int(item.price * Decimal("100")),
                    "currency": "usd",
                    "product_data": {
                        "name": item.product.name,
                    },
                },
                "quantity": item.quantity,
            })

        # Create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        # Redirect to Stripe payment form
        return redirect(session.url, code=303)
    else:
        return render(request, "payment/process.html", locals())


def payment_completed(request):
    return render(request, "payment/completed.html")


def payment_canceled(request):
    return render(request, "payment/canceled.html")