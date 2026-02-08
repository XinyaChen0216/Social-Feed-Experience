from django.db import models #model represents a database table

# Create Post and Media models

class Post(models.Model):
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id}"
#Post inherits from Django's base Model class, which makes it a database model

class Media(models.Model):
    MEDIA_TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )

    post = models.ForeignKey(
        Post,
        related_name='media', #allows reverse access
        on_delete=models.CASCADE # if a post is deleted, all its media are automatically deleted
    )
    file = models.FileField(upload_to='media/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)

    def __str__(self):
        return f"{self.media_type} for Post {self.post.id}"
