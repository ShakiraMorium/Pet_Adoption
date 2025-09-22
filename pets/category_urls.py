from django.urls import path
from pets import views

urlpatterns = [
    path('', views.ViewCategories.as_view(), name='category-list'),
    path('<int:pk>/', views.CategoryDetails.as_view(),
         name='view-specific-category')
]