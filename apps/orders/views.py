from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from apps.cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":

        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
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

        context = {"order": order}
        return render(request, "orders/order/created.html", context)

    elif request.method == "GET":
        form = OrderCreateForm()

    context = {
        "cart": cart,
        "form": form
    }
    return render(request, "orders/order/create.html", context)
