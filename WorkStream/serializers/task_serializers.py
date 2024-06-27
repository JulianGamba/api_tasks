from rest_framework import serializers

from WorkStream.models import CustomUser, Priority, State, Task

from .custom_user_serializers import CustomUserSerializer
from .priority_serializers import PrioritySerializer
from .state_serializers import StateSerializer


class TaskReadSerializer(serializers.ModelSerializer):
    state = StateSerializer()
    priority = PrioritySerializer()
    owner = CustomUserSerializer()
    assigned_users = CustomUserSerializer(many=True)

    class Meta:
        model = Task
        fields = "__all__"


# Serializador para la escritura
class TaskWriteSerializer(serializers.ModelSerializer):

    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    priority = serializers.PrimaryKeyRelatedField(queryset=Priority.objects.all())
    assigned_users = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), many=True
    )

    class Meta:

        model = Task
        exclude = ["owner"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["owner"] = user
        return super().create(validated_data)
