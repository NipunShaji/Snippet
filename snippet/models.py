from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):

    title = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.title


class Snippet(models.Model):

    title = models.CharField(max_length=128)
    content = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='snippets')

    def __str__(self):
        return self.title

