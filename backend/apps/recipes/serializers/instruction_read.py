from rest_framework import serializers
from apps.recipes.models.instruction import Instruction

class InstructionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ["id", "step_number", "description", "image"]
        read_only_fiels = fields
        