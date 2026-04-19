from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer



# User Registration Serializer (for creating accounts)
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'first_name',
                  'last_name', 'address', 'phone_number']
        # extra_kwargs = {'password': {'write_only': True}}


# User Serializer (for profile & safe responses)

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = ['id', 'email', 'first_name',
                  'last_name', 'address', 'phone_number']
