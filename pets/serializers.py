from rest_framework import serializers
from decimal import Decimal
from pets.models import PetCategory, Pet, PetImage, PetReview, AdoptionRequest
from django.contrib.auth import get_user_model



# Pet Category Serializer

class PetCategorySerializer(serializers.ModelSerializer):
    pet_count = serializers.IntegerField(
        read_only=True,
        help_text="Number of pets in this category"
    )

    class Meta:
        model = PetCategory
        fields = ['id', 'name', 'description', 'pet_count']



# Pet Image Serializer

class PetImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = PetImage
        fields = ['id', 'image']




# Pet Serializer

class PetSerializer(serializers.ModelSerializer):
    images = PetImageSerializer(many=True, read_only=True)
    adoption_fee_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'description', 'age', 'adoption_fee',
            'adoption_fee_with_tax', 'available', 'category', 'images'
        ]

    def calculate_tax(self, pet):
        # Example: add 10% tax to adoption fee
        return round(pet.adoption_fee * Decimal(1.1), 2)

    def validate_adoption_fee(self, adoption_fee):
        if adoption_fee < 0:
            raise serializers.ValidationError('Adoption fee cannot be negative')
        return adoption_fee



# Simple User Serializer

class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_current_user_name')

    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

    def get_current_user_name(self, obj):
        return obj.get_full_name()



# Pet Review Serializer

class PetReviewSerializer(serializers.ModelSerializer):
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



# Adoption Request Serializer

class AdoptionRequestSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    pet = PetSerializer(read_only=True)

    class Meta:
        model = AdoptionRequest
        fields = ['id', 'user', 'pet', 'message', 'approved', 'requested_at']
        read_only_fields = ['user', 'pet', 'approved', 'requested_at']
