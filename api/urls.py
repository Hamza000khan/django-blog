from django.urls import path
from .views import getAllBlogs, getBlogById, createBlog, updateBlog, deleteBlog, register, getBlogByUser, likeBlog, updateBlogAdmin
urlpatterns = [
    path('register/', register, name='register'),
    path('blogs/', getAllBlogs, name='blogs'),
    path('blogs/<int:pk>', getBlogById, name='blog'),
    path('user/blogs/', getBlogByUser, name='user-blogs'),
    path('blog/', createBlog, name='create-blog'),
    path('blog/<int:pk>', updateBlog, name='update-blog'),
    path('edit-blog/<int:pk>', updateBlogAdmin, name='update-blog'),
    path('delete/<int:pk>', deleteBlog, name='delete-blog'),
    path('like/<int:pk>', likeBlog, name='like-blog'),
]
