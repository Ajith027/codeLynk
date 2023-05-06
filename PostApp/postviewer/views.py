from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from postcreator.models import *
from .serializers import *
from django.db.models import F, Q, Count
from  .models import *
from .paginator import Pagination
from . functions import CsrfExemptSessionAuthentication


class usercreate(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    def post(self,request):
        name = request.data.get('username')
        password = request.data.get('password')
        if name and password:
            password = make_password(password)
            obj = User.objects.create(username=name,password=password)
            return JsonResponse({'status': "success",'message':'User created successfully'})
        return JsonResponse({'status': "error",'message':'please provide username and password'})

class userlogin(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication)
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.user
            login(request,user)
            return JsonResponse({'status': "success",'message':'User login successfully'})
        return JsonResponse({'status': "error",'message':'invalid ligin credentials'})

class Logout(APIView):
    def get(self,request):
        if request.user:
            logout(request)
            return JsonResponse({'status': "success",'message':'logout successfully'})
        return JsonResponse({'status': "error", 'message': 'FirstLogin'})

class All_posts(APIView):
    def get(self,request):
        try:
            #work flow for list similar post if a user previously liked a post
            viewed_post = ViewedPost.objects.filter(user=request.user)
            last_post = viewed_post.last()
            tag_name = Tags.objects.filter(post_id=last_post.post_id).values_list('name',flat=True).order_by('-weight')
            sim_post = Tags.objects.filter(name__in=tag_name).values_list('post_id',flat=True)
            data=[]
            for i in tag_name:
                a = Tags.objects.filter(name=i).exclude(post_id=last_post.post_id)
                for j in a:
                    data.append(j.post_id)

            # work flow for list similar post if a user previously  unliked a post
            if last_post.unlike == True:
                data = Post.objects.all().exclude(id__in=sim_post)

            # if user previously liked a post and no similar post found
            if not data:
                obj = viewed_post.values_list('post_id',flat=True)
                data = Post.objects.all().exclude(id__in=obj)
                if not data:
                    return JsonResponse({'status': "success", 'message': 'No NewPost'})
            pageitems = request.GET.get('pageitems', len(data))
            if pageitems == '':
                pageitems = len(data)
            if pageitems == 0:
                pageitems = 1
            paginator = Pagination(pageitems)
            page_data = paginator.paginate_queryset(data, request)
            serializer = PostSerializer(page_data, many=True)
            return paginator.get_paginated_response(serializer.data)
        except:
            obj = Post.objects.all()
            pageitems = request.GET.get('pageitems', obj.count())
            if pageitems == '':
                pageitems = obj.count()
            if pageitems == 0:
                pageitems = 1
            paginator = Pagination(pageitems)
            page_data = paginator.paginate_queryset(obj, request)
            serializer = PostSerializer(page_data,many=True)
            return paginator.get_paginated_response(serializer.data)

class To_likepost(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self,request):
        id = request.GET.get('id')
        try:
            obj = Post.objects.get(id=id)
        except:
            return JsonResponse({'status': "error", 'data': 'InvalidId'})
        try:
            user_post = ViewedPost.objects.get(user=request.user, post_id=obj)
        except:
            user_post = ViewedPost.objects.create(user=request.user, post_id=obj, like=True)
            obj.likes = F('likes') + 1
            user_post.save()
            obj.save()
            obj.refresh_from_db()
            serializer = PostSerializer(obj)
            return JsonResponse({'status': "success", 'data': serializer.data})
        if user_post.like == True:
            return JsonResponse({'status': "error", 'data': 'alreadyLiked'})
        user_post.like = True
        user_post.unlike = False
        obj.unlike = F('unlike') - 1
        obj.likes = F('likes') + 1
        user_post.save()
        obj.save()
        obj.refresh_from_db()
        serializer = PostSerializer(obj)
        return JsonResponse({'status': "success", 'data': serializer.data},safe=False)


class To_unlikepost(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self,request):
        id = request.GET.get('id')
        try:
            obj = Post.objects.get(id=id)
        except:
            return JsonResponse({'status': "error", 'data': 'InvalidId'})
        try:
            user_post = ViewedPost.objects.get(user=request.user, post_id=obj)
        except:
            user_post = ViewedPost.objects.create(user=request.user, post_id=obj, unlike=True)
            obj.unlike = F('unlike') + 1
            user_post.save()
            obj.save()
            obj.refresh_from_db()
            serializer = PostSerializer(obj)
            return JsonResponse({'status': "success", 'data': serializer.data})
        if user_post.unlike == True:
            return JsonResponse({'status': "error", 'data': 'already UnLiked'})
        user_post.like = False
        user_post.unlike = True
        obj.unlike = F('unlike') + 1
        obj.likes = F('likes') - 1
        user_post.save()
        obj.save()
        obj.refresh_from_db()
        serializer = PostSerializer(obj)
        return JsonResponse({'status': "success", 'data': serializer.data}, safe=False)




class All_usersLiked(APIView):

    def get(self,request):
        id = request.GET.get('id')
        try:
            obj = Post.objects.get(id=id)
        except:
            return JsonResponse({'status': "error", 'data': 'InvalidId'})
        posts = ViewedPost.objects.filter(Q(post_id=obj) & Q(like=True)).select_related('user')
        pageitems = request.GET.get('pageitems', posts.count())
        if pageitems == '':
            pageitems = posts.count()
        if pageitems == 0:
            pageitems = 1
        paginator = Pagination(pageitems)
        page_data = paginator.paginate_queryset(posts, request)
        serializer = UserSerializer(page_data, many=True)
        return paginator.get_paginated_response(serializer.data)
