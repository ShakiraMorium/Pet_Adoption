from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import PetUser


# User Registration Serializer (for creating accounts)
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = PetUser
        fields = [
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'address',
            'phone_number',
        ]
        # extra_kwargs = {'password': {'write_only': True}}


# User Serializer (for profile & safe responses)
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = PetUser
        ref_name = 'CustomUser'   # keep if you want unique schema name
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'address',
            'phone_number',
            'is_staff'
        ]
        read_only_fields = ['is_staff']
