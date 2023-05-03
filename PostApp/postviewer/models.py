from django.contrib.auth.models import User
from django.db import models
from postcreator.models import Post

# Create your models here.

class ViewedPost(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    unlike = models.BooleanField(default=False)
