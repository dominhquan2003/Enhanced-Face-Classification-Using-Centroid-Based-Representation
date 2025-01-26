# serializers.py
from rest_framework import serializers
from .models import Performer

class PerformerSerializer(serializers.ModelSerializer):
    original_image = serializers.ImageField(required=False)
    detected_image = serializers.ImageField(required=False)
    heatmap_1 = serializers.ImageField(required=False)
    heatmap_2 = serializers.ImageField(required=False)
    heatmap_3 = serializers.ImageField(required=False)
    class Meta:
        model = Performer
        fields = ['id', 'name', 'status', 'original_image', 'detected_image', 'heatmap_1', 'heatmap_2', 'heatmap_3']
        
    