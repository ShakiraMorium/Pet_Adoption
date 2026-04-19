from django.db.models import Count
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action
from django.views.generic import TemplateView, DetailView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from .permissions import IsAdminOrReadOnly, IsReviewAuthorOrReadOnly
from pets.models import Pet, PetCategory, PetImage, PetReview, CartRequest
from pets.serializers import (
    PetSerializer, CategorySerializer, PetImageSerializer, ReviewSerializer, CartRequestSerializer
)
from django.db.models import Count

# 1. UNCOMMENTED THE FILTER IMPORT
from pets.filters import PetFilter 
from pets.paginations import DefaultPagination  


# Pet ViewSet
class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # 2. UNCOMMENTED THE FILTERSET CLASS
    filterset_class = PetFilter 
    
    pagination_class = DefaultPagination
    search_fields = ['name', 'description']
    ordering_fields = ['adoption_fee', 'updated_at']
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        return Pet.objects.prefetch_related('images').all()
    
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
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    # This now works perfectly because we added related_name='pets' in models.py
    queryset = PetCategory.objects.annotate(
        pet_count=Count('pets') 
    ).all()


# Pet Review ViewSet
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]

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
        categories = PetCategory.objects.all()
        # 3. FIXED: Changed 'category=cat' to 'petCategory=cat'
        category_pets = {cat: Pet.objects.filter(petCategory=cat) for cat in categories} 
        context['category_pets'] = category_pets
        return context

class PetDetails(DetailView):
    model = Pet
    template_name = "pets/pet_detail.html"  
    context_object_name = "pet"
    pk_url_kwarg = "id"