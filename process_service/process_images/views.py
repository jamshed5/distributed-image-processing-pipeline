from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ProcessedImage
from .serializers import ProcessedImageSerializer

@api_view(['GET'])
def get_images(request):
    images = ProcessedImage.objects.all()
    serializer = ProcessedImageSerializer(images, many=True)
    return Response(serializer.data)