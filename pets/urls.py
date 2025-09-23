from django.urls import path

from pets import views

urlpatterns = [
    path('', views.PetListByCategoryView.as_view(), name='pet-list-by-category'),
    path('<int:id>/',views.PetDetails.as_view(), name='pet-list'),
]