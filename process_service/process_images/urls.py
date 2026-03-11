from django.urls import path
from .views import get_images

urlpatterns = [
    path('images/', get_images, name='get-images'),
]