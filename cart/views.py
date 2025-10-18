
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from cart.models import Cart, CartItem
from cart.serializers import (
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    EmptySerializer,
    UpdateCartSerializer,
    CreateCartSerializer,
)
from cart.services import CartService


# CART ITEM VIEWSET
class CartItemViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs.get('cart_pk')}

    def get_queryset(self):
        return CartItem.objects.select_related('pet').filter(
            cart_id=self.kwargs.get('cart_pk')
        )


#  MAIN CART VIEWSET
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'cancel':
            return EmptySerializer
        elif self.action == 'create':
            return CreateCartSerializer
        elif self.action == 'update_status':
            return UpdateCartSerializer
        return CartSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'user': self.request.user}

    def get_queryset(self):
        #  Use correct related_name from model: items_cart
        if self.request.user.is_staff:
            return Cart.objects.prefetch_related('items_cart__pet').all()
        return Cart.objects.prefetch_related('items_cart__pet').filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    #  Create or Return existing cart
    def create(self, request, *args, **kwargs):
        existing_cart = Cart.objects.filter(user=request.user).first()
        if existing_cart:
            serializer = self.get_serializer(existing_cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)

    #  Cancel Adoption (Cart)
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        cart = self.get_object()
        CartService.cancel_cart(cart=cart, user=request.user)
        return Response({'status': 'Adoption canceled'})

    #  Update Cart (status)
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        cart = self.get_object()
        serializer = UpdateCartSerializer(cart, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': f"Cart status updated to {request.data['status']}"})
