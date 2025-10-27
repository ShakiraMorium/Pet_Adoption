from rest_framework import serializers
from decimal import Decimal
from pets.models import PetCategory, Pet, PetImage, PetReview, CartRequest
from django.contrib.auth import get_user_model
# from cart.models import Cart


#

    
    # def get_pets_count(self, obj):
    #     # obj is a PetCategory instance
    #     return obj.pets_set.count() 


# 1. Pet Image Serializer
class PetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetImage
        fields = ['id', 'image']
        
    # def get_image_url(self, obj):
    #     return obj.image.url
    
# 2.pet serializer
class PetSerializer(serializers.ModelSerializer):
    images = PetImageSerializer(many=True, read_only=True)
    adoption_fee_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')  # move here

    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'description', 'age', 'adoption_fee',
            'adoption_fee_with_tax', 'is_available', 'category', 'images'
        ]

    # def get_adoption_fee_with_tax(self, obj):
    #     return round(obj.adoption_fee * Decimal(1.1), 2)
    def calculate_tax(self, pet):
        return round(pet.adoption_fee * Decimal(1.1), 2)

    def validate_adoption_fee(self, adoption_fee):
        if adoption_fee < 0:
            raise serializers.ValidationError("Adoption fee cannot be negative")
        return adoption_fee
    
# 3. Pet Category Serializer
# class PetCategorySerializer(serializers.ModelSerializer):
#     #  pets = PetSerializer(many=True, read_only=True, source='pet_set')

#     class Meta:
#         model = PetCategory
#         fields = ['id', 'name', 'description', 'pet_count']   
#         # pet_count = serializers.SerializerMethodField()     
#         pet_count = serializers.IntegerField(
#         read_only=True, help_text="Return the number pet in this category")

class PetCategorySerializer(serializers.ModelSerializer):
    # pets = PetSerializer(many=True, read_only=True, source='pet_count')
    # pets = serializers.SerializerMethodField()
    pet_count = serializers.SerializerMethodField()

    class Meta:
        model = PetCategory
        fields = ['id', 'name', 'description', 'pet_count', 'pets']

    # def get_pet_count(self, obj):
    #     return obj.pets.count()  # uses related_name

    # def get_pets(self, obj):
    #     pets_qs = obj.pets.all()[:4]  # show first 4 pets only
    #     return PetSerializer(pets_qs, many=True, context=self.context).data

    def get_pet_count(self, obj):
        return obj.pets.count() 

# 4. Simple User Serializer
class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_current_user_name')

    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

    def get_current_user_name(self, obj):
        return obj.get_full_name()


# 5. Pet Review Serializer
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


# 6. Adoption Request Serializer
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