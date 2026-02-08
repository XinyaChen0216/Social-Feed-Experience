# Register your models here.

from django.contrib import admin
from .models import Post, Media

# register Post and Media in admin panel -> make models manageable through the 
# Django Admin interface
admin.site.register(Post)
admin.site.register(Media)

