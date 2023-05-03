from django.db import models
from datetime import datetime
# Create your models here.


class Post(models.Model):
    desc = models.TextField(blank=True,null=True)
    likes = models.PositiveIntegerField(default=0)
    unlike = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


class Images(models.Model):
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    img = models.ImageField(upload_to='post_image',blank=True)



class Tags(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,blank=True)
    weight = models.IntegerField(default=0)





