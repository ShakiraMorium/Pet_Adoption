from rest_framework import serializers
from cart.models import Cart, CartItem, Cart, CartItem
from pets.models import Pet
from pets.serializers import PetSerializer
from cart.services import CartService


class EmptySerializer(serializers.Serializer):
    pass


# Simple Pet Serializer
class SimplePetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'adoption_fee']


# Add Cart Item Serializer
class AddCartItemSerializer(serializers.ModelSerializer):
    pet_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'pet_id', 'quantity']

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        pet_id = self.validated_data['pet_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, pet_id=pet_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data
            )

        return self.instance

    def validate_pet_id(self, value):
        if not Pet.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                f"Pet with id {value} does not exist"
            )
        return value


# Update Cart Item
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


# Cart Item Serializer
class CartItemSerializer(serializers.ModelSerializer):
    pet = SimplePetSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = CartItem
        fields = ['id', 'pet', 'quantity', 'total_price']

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.pet.adoption_fee


# Cart Serializer
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']
        read_only_fields = ['user']

    def get_total_price(self, cart: Cart):
        return sum(
            [item.pet.cart_fee * item.quantity for item in cart.items.all()]
        )


# Create Adoption (formerly Order)
class CreateCartSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("No cart found with this id")

        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError("Cart is empty")

        return cart_id

    def create(self, validated_data):
        user_id = self.context['user_id']
        cart_id = validated_data['cart_id']

        try:
            cart = CartService.create_cart(
                user_id=user_id, cart_id=cart_id
            )
            return cart
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        return CartSerializer(instance).data


#cart Item Serializer
class CartItemSerializer(serializers.ModelSerializer):
    pet = SimplePetSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'pet', 'price', 'quantity', 'total_price']


# Update cart (status only)
class UpdateCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['status']


# cart Serializer
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'status', 'total_price', 'created_at', 'items']
