from rest_framework import serializers
from apps.recipes.models.cuisine import Cuisine

class CuisineSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    parent_name = serializers.CharField(source="parent.name", read_only=True)

    class Meta:
        model = Cuisine
        fields = ["id", "name", "parent", "parent_name", "subcategories"]
        
    def get_subcategories(self, obj):
        children = obj.subcategories.all()
        return CuisineSerializer(children, many=True, context=self.context).data
    
    def validate(self, data):
        parent = data.get("parent")
        if self.instance and parent and self.instance.id == parent.id:
            raise serializers.ValidationError("A cuisine cannot be its own parent.")
        return data