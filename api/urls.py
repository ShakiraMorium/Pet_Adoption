from django.urls import path, include
from rest_framework_nested import routers
from order.views import  CartItemViewSet, OrderViewset,initiate_payment,payment_cancel, payment_fail, payment_success, HasOrderedPet
from rest_framework_nested import routers

from pets.views import PetViewSet, PetCategoryViewSet, PetReviewViewSet, PetImageViewSet


# Base router
router = routers.DefaultRouter()
router.register('pets', PetViewSet, basename='pets')
router.register('categories', PetCategoryViewSet, basename='categories')
router.register('carts', CartItemViewSet, basename='carts')
router.register('orders', OrderViewset, basename='orders')



# Nested routes: reviews under pets
pet_router = routers.NestedDefaultRouter(router, 'pets', lookup='pet')
pet_router.register('reviews', PetReviewViewSet, basename='pet-reviews')
pet_router.register('images', PetImageViewSet,basename='pet-images')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-item')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(pet_router.urls)),
    path('', include(cart_router.urls)),
    
   # Djoser core endpoints (register, users, reset, etc.)
    path('auth/', include('djoser.urls')),
    # JWT endpoints (login/create, refresh, verify)
    path('auth/', include('djoser.urls.jwt')),
     path("payment/initiate/", initiate_payment, name="initiate-payment"),
    path("payment/success/", payment_success, name="payment-success"),
    path("payment/fail/", payment_fail, name="payment-fail"),
    path("payment/cancel/", payment_cancel, name="payment-cancel"),
    path('orders/has-ordered/<int:pet_id>/',
         HasOrderedPet.as_view()),
]

# from django.urls import path, include
# from rest_framework_nested import routers
# from order.views import CartItemViewSet, OrderViewset, initiate_payment, payment_cancel, payment_fail, payment_success, HasOrderedPet

# # ✅ 1. Create main router first
# router = routers.DefaultRouter()
# router.register('carts', CartItemViewSet, basename='carts')   # parent
# router.register('orders', OrderViewset, basename='orders')

# # ✅ 2. Now create nested router — after parent registered
# cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
# cart_router.register('items', CartItemViewSet, basename='cart-items')

# # ✅ 3. Combine all routes
# urlpatterns = [
#     path('', include(router.urls)),
#     path('', include(cart_router.urls)),

#     # extra payment endpoints
#     path('initiate-payment/', initiate_payment, name='initiate-payment'),
#     path('payment-success/', payment_success, name='payment-success'),
#     path('payment-fail/', payment_fail, name='payment-fail'),
#     path('payment-cancel/', payment_cancel, name='payment-cancel'),
#     path('has-ordered/', HasOrderedPet.as_view(), name='has-ordered'),
# ]
