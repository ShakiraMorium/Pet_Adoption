# from rest_framework import serializers
# from cart.models import Cart, CartItem
# from pets.models import Pet
# from pets.serializers import PetSerializer


# # Simple Pet Serializer
# class SimplePetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pet
#         fields = ['id', 'name', 'adoption_fee']


# # Add Cart Item Serializer
# class AddCartItemSerializer(serializers.ModelSerializer):
#     pet_id = serializers.IntegerField()

#     class Meta:
#         model = CartItem
#         fields = ['id', 'pet_id', 'quantity']

#     def save(self, **kwargs):
#         cart_id = self.context['cart_id']
#         pet_id = self.validated_data['pet_id']
#         quantity = self.validated_data['quantity']

#         try:
#             cart_item = CartItem.objects.get(cart_id=cart_id, pet_id=pet_id)
#             cart_item.quantity += quantity
#             cart_item.save()
#             self.instance = cart_item
#         except CartItem.DoesNotExist:
#             self.instance = CartItem.objects.create(
#                 cart_id=cart_id, **self.validated_data
#             )

#         return self.instance

#     def validate_pet_id(self, value):
#         if not Pet.objects.filter(pk=value).exists():
#             raise serializers.ValidationError(
#                 f"Pet with id {value} does not exist"
#             )
#         return value


# # Update Cart Item Serializer
# class UpdateCartItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartItem
#         fields = ['quantity']


# # Cart Item Serializer
# class CartItemSerializer(serializers.ModelSerializer):
#     pet = SimplePetSerializer(read_only=True)
#     total_price = serializers.SerializerMethodField()

#     class Meta:
#         model = CartItem
#         fields = ['id', 'pet', 'quantity', 'total_price']

#     def get_total_price(self, cart_item: CartItem):
#         return cart_item.quantity * cart_item.pet.adoption_fee


# # Main Cart Serializer
# class CartSerializer(serializers.ModelSerializer):
#     items_cart = CartItemSerializer(many=True, read_only=True)
#     total_price = serializers.SerializerMethodField()

#     class Meta:
#         model = Cart
#         fields = ['id', 'user', 'created_at', 'items_cart', 'total_price']
#         read_only_fields = ['user']

#     def get_total_price(self, cart: Cart):
#         return sum(
#             [item.pet.adoption_fee * item.quantity for item in cart.items_cart.all()]
#         )
