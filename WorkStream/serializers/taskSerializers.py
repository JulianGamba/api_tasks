from rest_framework import serializers
from WorkStream.models import Task
from WorkStream.models import CustomUser
from WorkStream.models import State
from WorkStream.models import Priority
from .stateSerializers import StateSerializer
from .prioritySerializers import PrioritySerializer
from .customUserSerializers import CustomUserSerializer

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


   
        
