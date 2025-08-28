from django_filters.rest_framework import FilterSet
from pets.models import Pet

class PetFilter(FilterSet):
    class Meta:
        model = Pet
        fields = {
            'category_id': ['exact'],   # Filter by pet category
            'age': ['gt', 'lt'],        # Filter by age greater than or less than
            'adoption_fee': ['gt', 'lt']  # Filter by adoption fee range
        }
