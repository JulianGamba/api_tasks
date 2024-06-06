from rest_framework import serializers
from WorkStream.models.state import State

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'
