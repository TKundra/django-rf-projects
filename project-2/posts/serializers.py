from rest_framework import serializers

from posts.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content", "created"]
    
    def validate_title(self, title):
        special_characters = "!@#$%^&*()-+?_=,<>/."
        if title and any(v in special_characters for v in title):
            raise serializers.ValidationError('No special characters allowed');
        return title;