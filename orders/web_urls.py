from django.urls import path

from . import web_views

app_name = 'orders'

urlpatterns = [
    path('', web_views.pet_catalog, name='catalog'),
    path('cart/', web_views.cart_detail, name='cart_detail'),
    path('cart/add/<int:pet_id>/', web_views.cart_add, name='cart_add'),
    path('cart/update/<int:pet_id>/', web_views.cart_update, name='cart_update'),
    path('cart/remove/<int:pet_id>/', web_views.cart_remove, name='cart_remove'),
    path('checkout/', web_views.checkout, name='checkout'),
    path('checkout/success/<uuid:order_id>/', web_views.checkout_success, name='checkout_success'),
]