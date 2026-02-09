from django.shortcuts import render

# Create your views here.
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Post, Media
from .serializers import PostSerializer


# Adjust these to your requirements
ALLOWED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_VIDEO_EXTS = {".mp4", ".mov"}
MAX_IMAGE_BYTES = 10 * 1024 * 1024   # 10MB
MAX_VIDEO_BYTES = 50 * 1024 * 1024   # 50MB


def _detect_media_type(ext: str) -> str | None:
    ext = ext.lower()
    if ext in ALLOWED_IMAGE_EXTS:
        return "image"
    if ext in ALLOWED_VIDEO_EXTS:
        return "video"
    return None


class PostListCreateAPIView(APIView):
    """
    GET  /api/posts/   -> list posts latest first
    POST /api/posts/   -> create post with text + multiple files (images/videos)
    """
#when someone visits /api/posts, this method runs
    def get(self, request):
        posts = Post.objects.all().order_by("-created_at")
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        text = (request.data.get("text") or "").strip()
        files = request.FILES.getlist("files")  

        if not text and not files:
            return Response(
                {"detail": "Post must include text or at least one media file."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the Post model first
        post = Post.objects.create(text=text)

        # Validate + create Media model
        for f in files:
            ext = os.path.splitext(f.name)[1].lower()
            media_type = _detect_media_type(ext)
            if media_type is None:
                post.delete()
                return Response(
                    {"detail": f"Unsupported file type: {ext}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            size = getattr(f, "size", 0)
            if media_type == "image" and size > MAX_IMAGE_BYTES:
                post.delete()
                return Response(
                    {"detail": f"Image too large (max {MAX_IMAGE_BYTES} bytes): {f.name}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if media_type == "video" and size > MAX_VIDEO_BYTES:
                post.delete()
                return Response(
                    {"detail": f"Video too large (max {MAX_VIDEO_BYTES} bytes): {f.name}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            Media.objects.create(post=post, file=f, media_type=media_type)

        # Return the created post (with nested media)
        serializer = PostSerializer(post, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
