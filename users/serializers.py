from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer

# User Registration Serializer
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = BaseUserCreateSerializer.Meta.model
        fields = [
            'id', 'email', 'password', 'first_name',
            'last_name'
        ]

# User Serializer for Profile
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = BaseUserSerializer.Meta.model
        ref_name = 'CustomUser'
        fields = [
            'id', 'email', 'first_name',
            'last_name'
        ]
