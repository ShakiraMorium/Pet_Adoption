# api/views.py
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from pets.models import Pet
from .serializers import PetSerializer

# Custom pagination for pets
class PetPagination(PageNumberPagination):
    page_size = 10  # Number of pets per page
    page_size_query_param = 'page_size'
    max_page_size = 50

# List and Create Pets (paginated)
class PetListAPI(generics.ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    pagination_class = PetPagination  # enable pagination

# Retrieve, Update, Delete a single pet by ID
class PetDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    lookup_field = 'id'  # if your URL is <int:id>
