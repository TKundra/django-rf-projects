from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')    # reverse relationship, help to get each post created by author -> author.posts

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["-created"]
