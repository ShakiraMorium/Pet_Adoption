from django.db.models import Count
from django.views.generic import TemplateView, DetailView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from .permissions import IsAdminOrReadOnly, IsReviewAuthorOrReadonly
from pets.models import Pet, PetCategory, PetImage, PetReview, CartRequest
from pets.serializers import (
    PetSerializer, PetCategorySerializer, PetImageSerializer, PetReviewSerializer, CartRequestSerializer
)
from django.db.models import Count
from pets.filters import PetFilter
from pets.paginations import DefaultPagination  




# Pet ViewSet

class PetViewSet(ModelViewSet):
    
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PetFilter
    pagination_class = DefaultPagination
    search_fields = ['name', 'description']
    ordering_fields = ['adoption_fee', 'updated_at']
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(operation_summary='Retrieve a list of pets')
    def list(self, request, *args, **kwargs):
        """Retrieve all pets"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a pet by admin",
        operation_description="Only admin can create a pet",
        request_body=PetSerializer,
        responses={
            201: PetSerializer,
            400: "Bad Request"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)



# Pet Image ViewSet

class PetImageViewSet(ModelViewSet):
    serializer_class = PetImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return PetImage.objects.filter(pet_id=self.kwargs.get('pet_pk'))

    def perform_create(self, serializer):
        serializer.save(pet_id=self.kwargs.get('pet_pk'))



# Pet Category ViewSet

class PetCategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = PetCategory.objects.annotate(
        pet_count=Count('pets')).all()
    serializer_class = PetCategorySerializer



# class PetCategoryViewSet(ModelViewSet):
#     serializer_class = PetCategorySerializer
#     queryset = PetCategory.objects.annotate(
#         pet_count=Count('pets') 
#     ).all()


# Pet Review ViewSet

class PetReviewViewSet(ModelViewSet):
    serializer_class = PetReviewSerializer
    permission_classes = [IsReviewAuthorOrReadonly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return PetReview.objects.filter(pet_id=self.kwargs.get('pet_pk'))

    def get_serializer_context(self):
        return {'pet_id': self.kwargs.get('pet_pk')}



# Adoption Request ViewSet

class CartRequestViewSet(ModelViewSet):
    serializer_class = CartRequestSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return CartRequest.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PetListByCategoryView(TemplateView):
    template_name = "pets/pet_list_by_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all categories with their pets
        categories = PetCategory.objects.all()
        category_pets = {cat: Pet.objects.filter(category=cat) for cat in categories}
        context['category_pets'] = category_pets
        return context

class PetDetails(DetailView):
        model = Pet
        template_name = "pets/pet_detail.html"  # template for single pet
        context_object_name = "pet"
        pk_url_kwarg = "id"  # matches <int:id> in urls.py