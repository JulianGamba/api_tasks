from rest_framework import serializers
from WorkStream.models import CustomUser 
class CustomUserSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'email', 'full_name', 'avatar', 'birth_date', 'identification')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            full_name=validated_data.get('full_name', ''),
            avatar=validated_data.get('avatar', None),
            birth_date=validated_data.get('birth_date', None),
            identification=validated_data.get('identification', None),
        )
        return user
