
from rest_framework import serializers
from WorkStream.models.tasks import Task
from WorkStream.models.customUser import CustomUser
from WorkStream.models.state import State
from WorkStream.models.priority import Priority
from WorkStream.serializers.customUserSerializers import CustomUserSerializer
from .loginSerializers import LoginSerializer
from WorkStream.serializers.prioritySerializers import PrioritySerializer
from WorkStream.serializers.stateSerializers import StateSerializer



class TaskReadSerializer(serializers.ModelSerializer):
    state = StateSerializer()
    priority = PrioritySerializer()
    owner = CustomUserSerializer()
    assigned_users = CustomUserSerializer(many=True)

    class Meta:
        model = Task
        fields = '__all__'

# Serializador para la escritura
class TaskWriteSerializer(serializers.ModelSerializer):
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    priority = serializers.PrimaryKeyRelatedField(queryset=Priority.objects.all())
    assigned_users = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)

    class Meta:
        model = Task
        exclude = ['owner']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        return super().create(validated_data)
