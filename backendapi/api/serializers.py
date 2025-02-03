# serializers.py
from rest_framework import serializers
from .models import Performer

class PerformerSerializer(serializers.ModelSerializer):
    original_image = serializers.ImageField(required=False, allow_null=True)
    detected_image = serializers.ImageField(required=False, allow_null=True)
    heatmap_1 = serializers.ImageField(required=False, allow_null=True)
    heatmap_2 = serializers.ImageField(required=False, allow_null=True)
    heatmap_3 = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Performer
        fields = ['id', 'name', 'status', 'original_image', 'detected_image', 'heatmap_1', 'heatmap_2', 'heatmap_3']
