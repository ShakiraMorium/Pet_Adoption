from rest_framework import serializers
from pets.models import Pet, PetCategory, CartRequest
from users.models import PetUser
from order.models import Cart, CartItem, Order, OrderItem
from pets.serializers import PetSerializer
from order.services import OrderService
from cart.serializers import AddCartItemSerializer

class EmptySerializer(serializers.Serializer):
    pass


class SimplePetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'age', 'category']


# Adding a pet to adoption request
class AddCartItemSerializer(serializers.ModelSerializer):
    pet_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'pet_id', 'quantity']

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        pet_id = self.validated_data['pet_id']
        quantity = self.validated_data.get('quantity')

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=pet_id)
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    def validate_pet_id(self, value):
        if not Pet.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"Pet with id {value} does not exist")
        return value


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartItemSerializer(serializers.ModelSerializer):
    pet = SimplePetSerializer()
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')
    class Meta:
        model = CartItem
        fields = ['id', 'pet', 'quantity','total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'total_price','items',]
        read_only_fields = ['user']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart found with this id')

        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Cart is empty')

        return cart_id

    def create(self, validated_data):
        user_id = self.context['user_id']
        cart_id = validated_data['cart_id']

        try:
            order = OrderService.create_order(user_id=user_id, cart_id=cart_id)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        return OrderSerializer(instance).data


    class AddCartItemSerializer(serializers.ModelSerializer):
        pet = SimplePetSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'pet', 'price', 'quantity', 'total_price']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']


class OrderSerializer(serializers.ModelSerializer):
    items = AddCartItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'created_at', 'items']