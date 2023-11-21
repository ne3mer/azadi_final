from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='images', blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
