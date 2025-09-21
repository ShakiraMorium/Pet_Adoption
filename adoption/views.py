from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# from django.http import HttpResponseRedirect

from adoption import serializers as adoptionSz
from adoption.serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from adoption.models import Cart, CartItem, Adoption, AdoptionItem
from adoption.services import AdoptionService
# from sslcommerz_python.payment import SSLCOMMERZ
from django.conf import settings as main_settings


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items__pet').filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        existing_cart = Cart.objects.filter(user=request.user).first()
        if existing_cart:
            serializer = self.get_serializer(existing_cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context
        return {'cart_id': self.kwargs.get('cart_pk')}

    def get_queryset(self):
        return CartItem.objects.select_related('pet').filter(cart_id=self.kwargs.get('cart_pk'))


class AdoptionViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'patch', 'head', 'options']

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        adoption = self.get_object()
        AdoptionService.cancel_adoption(adoption=adoption, user=request.user)
        return Response({'status': 'Adoption canceled'})

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        adoption = self.get_object()
        serializer = adoptionSz.UpdateAdoptionSerializer(
            adoption, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': f"Adoption status updated to {request.data['status']}"})

    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'cancel':
            return adoptionSz.EmptySerializer
        if self.action == 'create':
            return adoptionSz.CreateAdoptionSerializer
        elif self.action == 'update_status':
            return adoptionSz.UpdateAdoptionSerializer
        return adoptionSz.AdoptionSerializer

    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        return {'user_id': self.request.user.id, 'user': self.request.user}

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Adoption.objects.none()
        if self.request.user.is_staff:
            return Adoption.objects.prefetch_related('items__pet').all()
        return Adoption.objects.prefetch_related('items__pet').filter(user=self.request.user)


# ================== PAYMENT ==================

# @api_view(['POST'])
# def initiate_payment(request):
#     user = request.user
#     amount = request.data.get("amount")
#     adoption_id = request.data.get("adoptionId")
#     num_items = request.data.get("numItems")

#     settings_conf = {
#         'store_id': 'your_store_id',
#         'store_pass': 'your_store_pass',
#         'issandbox': True
#     }
#     sslcz = SSLCOMMERZ(settings_conf)

#     post_body = {
#         'total_amount': amount,
#         'currency': "BDT",
#         'tran_id': f"txn_{adoption_id}",
#         'success_url': f"{main_settings.BACKEND_URL}/api/v1/payment/success/",
#         'fail_url': f"{main_settings.BACKEND_URL}/api/v1/payment/fail/",
#         'cancel_url': f"{main_settings.BACKEND_URL}/api/v1/payment/cancel/",
#         'emi_option': 0,
#         'cus_name': f"{user.first_name} {user.last_name}",
#         'cus_email': user.email,
#         'cus_phone': user.phone_number,
#         'cus_add1': user.address,
#         'cus_city': "Dhaka",
#         'cus_country': "Bangladesh",
#         'shipping_method': "Courier",
#         'num_of_item': num_items,
#         'product_name': "Pet Adoption",
#         'product_category': "Pets",
#         'product_profile': "general",
#     }

#     response = sslcz.createSession(post_body)
#     if response.get("status") == 'SUCCESS':
#         return Response({"payment_url": response['GatewayPageURL']})
#     return Response({"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def payment_success(request):
#     adoption_id = request.data.get("tran_id").split('_')[1]
#     adoption = Adoption.objects.get(id=adoption_id)
#     adoption.status = "Ready To Ship"
#     adoption.save()
#     return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/adoptions/")


# @api_view(['POST'])
# def payment_cancel(request):
#     return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/adoptions/")


# @api_view(['POST'])
# def payment_fail(request):
#     return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/adoptions/")


# class HasAdoptedPet(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pet_id):
#         user = request.user
#         has_adopted = AdoptionItem.objects.filter(
#             adoption__user=user, pet_id=pet_id
#         ).exists()
#         return Response({"hasAdopted": has_adopted})
