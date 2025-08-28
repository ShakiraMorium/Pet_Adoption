from rest_framework import serializers
from pets.models import Pet, Category, AdoptionRequest, RequestedPet, Adoption, AdoptionPet
from users.models import User


class EmptySerializer(serializers.Serializer):
    pass


class SimplePetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'age', 'category']


# Adding a pet to adoption request
class AddRequestedPetSerializer(serializers.ModelSerializer):
    pet_id = serializers.IntegerField()

    class Meta:
        model = RequestedPet
        fields = ['id', 'pet_id', 'quantity']

    def save(self, **kwargs):
        adoption_request_id = self.context['adoption_request_id']
        pet_id = self.validated_data['pet_id']
        quantity = self.validated_data.get('quantity', 1)

        try:
            requested_pet = RequestedPet.objects.get(
                adoption_request_id=adoption_request_id, pet_id=pet_id)
            requested_pet.quantity += quantity
            requested_pet.save()
            self.instance = requested_pet
        except RequestedPet.DoesNotExist:
            self.instance = RequestedPet.objects.create(
                adoption_request_id=adoption_request_id, **self.validated_data
            )
        return self.instance

    def validate_pet_id(self, value):
        if not Pet.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"Pet with id {value} does not exist")
        return value


class UpdateRequestedPetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestedPet
        fields = ['quantity']


class RequestedPetSerializer(serializers.ModelSerializer):
    pet = SimplePetSerializer()
    class Meta:
        model = RequestedPet
        fields = ['id', 'pet', 'quantity']


class AdoptionRequestSerializer(serializers.ModelSerializer):
    requested_pets = RequestedPetSerializer(many=True, read_only=True)

    class Meta:
        model = AdoptionRequest
        fields = ['id', 'user', 'requested_pets']
        read_only_fields = ['user']


class CreateAdoptionSerializer(serializers.Serializer):
    adoption_request_id = serializers.UUIDField()

    def validate_adoption_request_id(self, adoption_request_id):
        if not AdoptionRequest.objects.filter(pk=adoption_request_id).exists():
            raise serializers.ValidationError('No adoption request found with this id')

        if not RequestedPet.objects.filter(adoption_request_id=adoption_request_id).exists():
            raise serializers.ValidationError('No pets added to adoption request')

        return adoption_request_id

    def create(self, validated_data):
        user_id = self.context['user_id']
        adoption_request_id = validated_data['adoption_request_id']

        adoption_request = AdoptionRequest.objects.get(pk=adoption_request_id)
        adoption = Adoption.objects.create(user_id=user_id)

        for requested_pet in adoption_request.requested_pets.all():
            AdoptionPet.objects.create(
                adoption=adoption,
                pet=requested_pet.pet,
                quantity=requested_pet.quantity
            )
            # Mark pet as adopted
            requested_pet.pet.is_adopted = True
            requested_pet.pet.save()

        return adoption

    def to_representation(self, instance):
        return AdoptionSerializer(instance).data


class AdoptionPetSerializer(serializers.ModelSerializer):
    pet = SimplePetSerializer()

    class Meta:
        model = AdoptionPet
        fields = ['id', 'pet', 'quantity']


class UpdateAdoptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = ['status']


class AdoptionSerializer(serializers.ModelSerializer):
    adopted_pets = AdoptionPetSerializer(many=True)

    class Meta:
        model = Adoption
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'adopted_pets']
