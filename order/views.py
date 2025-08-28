from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from pets.models import AdoptionRequest, RequestedPet, Adoption, AdoptionPet
from pets import serializers as petSz



class AdoptionRequestViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    """
    Handles creating, retrieving, and deleting adoption requests (like cart)
    """
    serializer_class = petSz.AdoptionRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return AdoptionRequest.objects.none()
        return AdoptionRequest.objects.prefetch_related('requested_pets__pet').filter(user=self.request.user)


class RequestedPetViewSet(ModelViewSet):
    """
    Handles adding/removing/updating pets inside an adoption request
    """
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return petSz.AddRequestedPetSerializer
        elif self.request.method == 'PATCH':
            return petSz.UpdateRequestedPetSerializer
        return petSz.RequestedPetSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context
        return {'adoption_request_id': self.kwargs.get('adoption_request_pk')}

    def get_queryset(self):
        return RequestedPet.objects.select_related('pet').filter(adoption_request_id=self.kwargs.get('adoption_request_pk'))


class AdoptionViewSet(ModelViewSet):
    """
    Handles confirmed adoptions (like orders)
    """
    http_method_names = ['get', 'post', 'delete', 'patch', 'head', 'options']

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        adoption = self.get_object()
        AdoptionService.cancel_adoption(adoption=adoption, user=request.user)
        return Response({'status': 'Adoption canceled'})

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        adoption = self.get_object()
        serializer = petSz.UpdateAdoptionSerializer(adoption, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': f'Adoption status updated to {request.data["status"]}'})

    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'cancel':
            return petSz.EmptySerializer
        if self.action == 'create':
            return petSz.CreateAdoptionSerializer
        elif self.action == 'update_status':
            return petSz.UpdateAdoptionSerializer
        return petSz.AdoptionSerializer

    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        return {'user_id': self.request.user.id, 'user': self.request.user}

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Adoption.objects.none()
        if self.request.user.is_staff:
            return Adoption.objects.prefetch_related('adopted_pets__pet').all()
        return Adoption.objects.prefetch_related('adopted_pets__pet').filter(user=self.request.user)
