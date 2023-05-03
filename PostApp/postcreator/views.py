from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from .models import *
# Create your views here.

class home(View):
    def get(self,request):
        return render(request,'new.html')

    def post(self,request):
        images = request.FILES.getlist('images[]')
        tags = request.POST.getlist('tags[]')
        weights = request.POST.getlist('weights[]')
        desc =request.POST.get('description')
        try:
            if not images and tags :
                messages.info(request, 'Image and Tag is required')

        except:
            pass
        else:
            obj = Post.objects.create(desc=desc)
            for i in images:
                img_obj = Images.objects.create(post_id=obj, img=i)
            for i in range(len(tags)):
                tag_obj = Tags.objects.create(post_id=obj, name=tags[i], weight=weights[i])
            messages.info(request, 'Successfully Created')
        return render(request, 'new.html')

class showall(View):
    def get(self,request):
        obj = Post.objects.all()
        return render(request,'posts.html',{'obj':obj})