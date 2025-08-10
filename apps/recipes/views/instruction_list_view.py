from rest_framework import generics
from rest_framework import permissions
from apps.recipes.models.instruction import Instruction
from apps.recipes.serializers.instruction_serializer import InstructionSerializer

class InstructionListCreate(generics.ListCreateAPIView):
    queryset = Instruction.objects.all()
    serializer_class = InstructionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]