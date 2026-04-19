from rest_framework import serializers
from decimal import Decimal
from pets.models import PetCategory, Pet, PetImage, PetReview, CartRequest
from django.contrib.auth import get_user_model


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PetCategory
        fields = ['id', 'name', 'description', 'pet_count']

    pet_count = serializers.IntegerField(
        read_only=True, help_text="Return the number pet in this category")


class PetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetImage
        fields = ['id', 'image']


class PetSerializer(serializers.ModelSerializer):
    images = PetImageSerializer(many=True, read_only=True)

    class Meta:
        model = Pet
        fields = ['id', 
            'name', 
            'breed', 
            'age', 
            'price_with_tax',
            'description', 
            'adoption_fee', 
            'is_available', 
            'petCategory', 
            'images',  # <--- ADD THIS LINE HERE
            'created_at', 
            'updated_at']  # other

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, pet):
        return round(pet.adoption_fee * Decimal(1.1), 2)

    def validate_adoption_fee(self, adoption_fee):
        if adoption_fee < 0:
            raise serializers.ValidationError('Adoption fee could not be negative')
        return adoption_fee


class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(
        method_name='get_current_user_name')

    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

    def get_current_user_name(self, obj):
        return obj.get_full_name()


class ReviewSerializer(serializers.ModelSerializer):
    # user = SimpleUserSerializer()
    user = serializers.SerializerMethodField(method_name='get_user')

    class Meta:
        model = PetReview
        fields = ['id', 'user', 'pet', 'ratings', 'comment']
        read_only_fields = ['user', 'pet']

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data

    def create(self, validated_data):
        pet_id = self.context['pet_id']
        return PetReview.objects.create(pet_id=pet_id, **validated_data)


class CartRequestSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    pet = PetSerializer(read_only=True)

    pet_id = serializers.PrimaryKeyRelatedField(
        queryset=Pet.objects.all(), write_only=True
    )
    
    class Meta:
        model = CartRequest
        fields = ['id', 'user', 'pet', 'approved', 'requested_at']
        read_only_fields = ['user', 'pet', 'approved', 'requested_at']
    
    def create(self, validated_data):
        # Remove pet_id from validated_data and assign pet object
        pet = validated_data.pop('pet_id')
        user = self.context['request'].user  # current logged-in user
        cart_request = CartRequest.objects.create(
            user=user,
            pet=pet
        )
        return cart_request