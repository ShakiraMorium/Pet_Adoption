from django.urls import path
from pets import views

urlpatterns = [
    path('', views.PetList.as_view(), name='pet-list'),
    path('<int:id>/', views.PetDetails.as_view(), name='pet-list'),
]