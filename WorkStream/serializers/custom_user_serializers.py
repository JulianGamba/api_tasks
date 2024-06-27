from django.contrib.auth import get_user_model
from rest_framework import serializers

CustomUser = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "password",
            "email",
            "full_name",
            "avatar",
            "birth_date",
            "identification",
        )
        extra_kwargs = {"password": {"write_only": True}}
    def create(self, validated_data):
        # Crear el usuario con todos los campos necesarios
        user = CustomUser(
            email=validated_data['email'],
            full_name=validated_data.get('full_name', ''),
            avatar=validated_data.get('avatar', None),
            birth_date=validated_data.get('birth_date', None),
            identification=validated_data.get('identification', None),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
