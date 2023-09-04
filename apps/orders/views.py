import weasyprint
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from apps.cart.cart import Cart

from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":

        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in iter(cart):
                # TODO: Use BulkCreate instead?
                OrderItem.objects.create(
                    order=order,
                    product=item.get("product"),
                    price=item.get("price"),
                    quantity=item.get("quantity")
                )
            # Clear cart after saving order.
            cart.clear()

            # Send email on order creation
            order_created.delay(order.id)

            # Set order in session
            request.session['order_no'] = order.order_no

            # Redirect to payment processs
            return redirect(reverse("payment:process"))

        # context = {"order": order}
        # return render(request, "orders/order/created.html", context)

    else:
        form = OrderCreateForm()

    context = {
        "cart": cart,
        "form": form
    }
    return render(request, "orders/order/create.html", context)


@staff_member_required
def admin_order_detail(request, order_no):
    order = get_object_or_404(Order, order_no=order_no)

    context = {"order": order}
    return render(request, "admin/orders/order/detail.html", context)


@staff_member_required
def admin_order_pdf(request, order_no):
    order = get_object_or_404(Order, order_no=order_no)
    html = render_to_string(
        "orders/order/invoice_template.html",
        {"order": order}
    )
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f"filename=WHEELDEALSHOP-order-{order.order_no}.pdf"    # noqa
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    )
    return response
