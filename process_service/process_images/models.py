# models.py
from django.db import models

class ProcessedImage(models.Model):
    filename = models.CharField(max_length=255)
    image_file = models.ImageField(upload_to="processed_images/")  # stored in MEDIA_ROOT
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename