from django.urls import path

from .web_views import (
    CartAddView,
    CartDetailView,
    CartRemoveView,
    CartUpdateView,
    CheckoutSuccessView,
    CheckoutView,
    PaymentRedirectView,
    PetCatalogView,
    PetDetailView,
    UserDashboardView,
)


app_name = 'orders'

urlpatterns = [
    path('', PetCatalogView.as_view(), name='catalog'),
    path('pets/<int:pk>/', PetDetailView.as_view(), name='pet_detail'),
    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:pet_id>/', CartAddView.as_view(), name='cart_add'),
    path('cart/update/<int:pet_id>/', CartUpdateView.as_view(), name='cart_update'),
    path('cart/remove/<int:pet_id>/', CartRemoveView.as_view(), name='cart_remove'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout/success/<uuid:order_id>/', CheckoutSuccessView.as_view(), name='checkout_success'),
    path('checkout/pay/<uuid:order_id>/', PaymentRedirectView.as_view(), name='payment_redirect'),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
]