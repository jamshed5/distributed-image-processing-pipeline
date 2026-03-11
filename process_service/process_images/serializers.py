from rest_framework import serializers
from .models import ProcessedImage

class ProcessedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedImage
        fields = '__all__'