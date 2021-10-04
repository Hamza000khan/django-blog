from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(max_length=250)
    likes = models.IntegerField()
    user = models.ForeignKey(User, null=False, blank=False,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class LikedBlogs(models.Model):
    user = models.ForeignKey(User, null= False,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, null= True, on_delete=models.CASCADE)
