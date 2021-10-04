from django.contrib import admin
from .models import Blog, LikedBlogs

admin.site.register(Blog)
admin.site.register(LikedBlogs)