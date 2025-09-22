from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import PetUser

# User Registration Serializer
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = PetUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'address', 'phone_number']

# User Serializer for Profile
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = PetUser
        ref_name = 'CustomUser'
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'address', 'phone_number']
