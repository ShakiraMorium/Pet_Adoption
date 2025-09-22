from django.urls import path, include
from rest_framework_nested import routers
from pets.views import (
    PetViewSet,
    PetCategoryViewSet,
    PetReviewViewSet,
    AdoptionRequestViewSet,
    
)


# Base router
router = routers.DefaultRouter()
router.register('pets', PetViewSet, basename='pets')
router.register('categories', PetCategoryViewSet, basename='categories')
router.register('adoptions', AdoptionRequestViewSet, basename='adoptions')




# Nested routes: reviews under pets
pet_router = routers.NestedDefaultRouter(router, 'pets', lookup='pet')
pet_router.register('reviews', PetReviewViewSet, basename='pet-reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(pet_router.urls)),
   # Djoser core endpoints (register, users, reset, etc.)
    path('auth/', include('djoser.urls')),
    # JWT endpoints (login/create, refresh, verify)
    path('auth/', include('djoser.urls.jwt')),
]
