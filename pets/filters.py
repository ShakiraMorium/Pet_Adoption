from django_filters import rest_framework as filters
from .models import Pet

class PetFilter(filters.FilterSet):
    class Meta:
        model = Pet
        fields = {
            'petCategory': ['exact'],  # Must match the model exactly
            'name': ['icontains'],
            'description': ['icontains'],
        }