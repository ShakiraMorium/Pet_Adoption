from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from pets.models import Pet
from .serializers import PetSerializer

class PetListAPI(generics.ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class PetDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    lookup_field = 'id'  # if you use <int:id> in urls
