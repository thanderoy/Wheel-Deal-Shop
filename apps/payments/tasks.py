from io import BytesIO

import weasyprint
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from apps.orders.models import Order


@shared_task
def send_payment_receipt(order_id):
    """
    Task to send an email notification on successful payment of an order
        along with a receipt.

    """
    order = Order.objects.get(id=order_id)

    # Create invoice email
    client_reference = order.first_name or order.last_name or "there"
    subject = settings.SUBJECT_PREFIX + f"Wheel Deal Shop - Invoice No. {order.order_no}"   # noqa
    message = f"Hi, {client_reference}.\n\n \
        Please find attached the invoice for your recent purchase."
    email = EmailMessage(
        subject, message, settings.SHOP_EMAIL_ADDRESS, [order.email]
    )

    # Generate Invoice PDF
    html = render_to_string(
        "orders/order/invoice_template.html", {"order": order}
    )
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / "css/pdf.css")]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # Attach PDF and send email
    email.attach(
        f"order-{order.order_no}.pdf",
        out.getvalue(),
        'application/pdf'
    )
    email.send()
