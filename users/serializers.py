from djoser.serializers import UserSerializer

class UserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'address']