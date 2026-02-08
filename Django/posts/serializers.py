from rest_framework import serializers
from .models import Post, Media

#serializer: convert data between Django and JSON

class MediaSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField() # used to add a value to the JSON output

    class Meta:
        model = Media
        fields = ["id", "media_type", "url"]

    def get_url(self, obj):
        request = self.context.get("request")
        if not obj.file:
            return None
        # Absolute URL is nicer for Vue; falls back to relative if no request
        return request.build_absolute_uri(obj.file.url) if request else obj.file.url


class PostSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "text", "created_at", "media"]

