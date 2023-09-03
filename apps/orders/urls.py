from django.urls import path
from . import views


app_name = "orders"

urlpatterns = [
    path("create/", views.order_create, name="order_create"),
    path("admin/order/<str:order_no>/", views.admin_order_detail, name="admin_order_detail"),   # noqa
    path("admin/order/<str:order_no>/pdf", views.admin_order_pdf, name="admin_order_pdf")   # noqa
]
