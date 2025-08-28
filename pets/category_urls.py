from django.urls import path
from pets import views

urlpatterns = [
    # List all pet categories
    path('', views.ViewPetCategories.as_view(), name='pet-category-list'),

    # View details of a specific pet category
    path('<int:pk>/', views.PetCategoryDetails.as_view(), name='view-specific-pet-category'),
]
