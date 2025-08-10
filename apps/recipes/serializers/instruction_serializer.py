from rest_framework import serializers
from apps.recipes.models.instruction import Instruction

class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ['id', 'step_number', 'description', 'image']