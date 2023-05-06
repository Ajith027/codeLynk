from postcreator.models import *
from .models import *
from rest_framework import serializers

class ImageSerializer(serializers.Serializer):
    img =serializers.ImageField()

class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    images = serializers.SerializerMethodField()
    desc = serializers.CharField()
    liked = serializers.SerializerMethodField()
    disliked = serializers.SerializerMethodField()
    likes = serializers.IntegerField(read_only=True)
    unlike = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField()

    def get_images(self,obj):
        img_obj = Images.objects.filter(post_id=obj)
        serializer = ImageSerializer(img_obj,many=True)
        return serializer.data
    def get_liked(self,obj):
        try:
            ob = ViewedPost.objects.get(post_id=obj.id)
            return ob.like
        except:
            return False
    def get_disliked(self,obj):
        try:
            ob = ViewedPost.objects.get(post_id=obj)
            return ob.unlike
        except:
            return False


    def to_representation(self, instance):
        data = super(PostSerializer, self).to_representation(instance)
        data['total_likes'] = data.pop('likes')
        data['total_dislikes'] = data.pop('unlike')
        return data


class UserSerializer(serializers.Serializer):
    username = serializers.SerializerMethodField()
    def get_username(self,obj):
        name = obj.user.username
        return name
