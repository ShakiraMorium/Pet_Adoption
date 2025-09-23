from django.urls import path, include
from rest_framework_nested import routers
from order.views import  CartItemViewSet, OrderViewset
from order.views import OrderViewset
from pets.views import (
    PetViewSet,
    PetCategoryViewSet,
    PetReviewViewSet,
    CartRequestViewSet,PetImageViewSet
    
)


# Base router
router = routers.DefaultRouter()
router.register('pets', PetViewSet, basename='pets')
router.register('categories', PetCategoryViewSet, basename='categories')
router.register('carts', CartRequestViewSet, basename='carts')
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
]
