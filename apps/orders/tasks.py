from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings


@shared_task
def order_created(order_id):
    """
    Task to send an email notification when an order is
        successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = settings.SUBJECT_PREFIX + f"Order No. {order.order_no}"
    message = f"Dear {order.first_name}, \n\n" \
        f"You have successfully placed and order." \
        f"Your order ID is {order.order_no}."
    mail_sent = send_mail(
        subject,
        message,
        "roy.thande@gmail.com",
        [order.email]
    )
    return mail_sent
