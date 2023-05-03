from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from postcreator.models import *
from .serializers import *
from django.db.models import F, Q, Count
from  .models import *

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class usercreate(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self,request):
        name = request.data.get('username')
        password = request.data.get('password')
        print(request.data.get('username'))
        print(name)
        if name and password :
            password = make_password(password)
            obj = User.objects.create(username=name,password=password)
            return JsonResponse({'status': "success",'message':'User created successfully'})
        return JsonResponse({'status': "error",'message':'please provide username and password'})

class userlogin(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,BasicAuthentication)

    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
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

from .paginator import Pagination
class All_posts(APIView):

    def get(self,request):
        try:
            sim_post = ViewedPost.objects.filter(user=request.user).last()
            tag = Tags.objects.filter(post_id=sim_post.post_id)
            queryset = tag.annotate(count=Count('id')).order_by('-weight')
            name=[]
            for i in queryset:
                name.append(i.name)
            new_data=[]
            dis=[]
            data=[]
            tags =Tags.objects.filter(name__in=name).exclude(post_id=sim_post.post_id)
            for i in tags:
                new_data.append(i.post_id)
            if sim_post.like:
                data=new_data
            else:
                for i in tags:
                    dis.append(i.post_id.id)
                data = Post.objects.all().exclude(id__in=dis)

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
            pass

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
            if obj:
                try:
                    user_post = ViewedPost.objects.get(user=request.user,post_id=obj)
                    if user_post.like:
                        return JsonResponse({'status': "error", 'data': 'alreadyLiked'})

                except:
                    user_post = ViewedPost.objects.create(user=request.user,post_id=obj, like=True)
                    obj.likes = F('likes') + 1
                if user_post:
                    user_post.like = True
                    user_post.unlike = False
                    user_post.save()
                    obj.unlike = F('unlike') - 1
                    obj.save()
                    return JsonResponse({'status': "success", 'data': 'likedSuccessfully'})
        except :
            return JsonResponse({'status': "error", 'data': 'InvalidId'})

class To_unlikepost(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self,request):
        id = request.GET.get('id')
        print(request.user.username)
        try:
            obj = Post.objects.get(id=id)
            print(obj)
            if obj:

                try:
                    user_post = ViewedPost.objects.get(user=request.user,post_id=obj)
                    if user_post.unlike:
                        return JsonResponse({'status': "error", 'data': 'alreadyDisliked'})

                except:
                    user_post = ViewedPost.objects.create(user=request.user,post_id=obj, unlike=True)
                    obj.unlike = F('unlike') + 1
                if user_post:
                    user_post.like = False
                    user_post.unlike = True
                    user_post.save()
                    obj.like = F('like') - 1
                    obj.save()
                    return JsonResponse({'status': "success", 'data':'unlikedSuccessfully' })
        except Exception as e :
            return JsonResponse({'status': "error", 'data':str(e)})

class All_usersLiked(APIView):

    def get(self,request):
        id = request.GET.get('id')
        try:
            obj = Post.objects.get(id=id)
        except Exception as e :
            return JsonResponse({'status': "error", 'data': str(e)})
        posts = ViewedPost.objects.filter(Q(post_id=obj)&Q(like=True)).select_related('user')
        pageitems = request.GET.get('pageitems', posts.count())
        if pageitems == '':
            pageitems = posts.count()
        if pageitems == 0:
            pageitems = 1
        paginator = Pagination(pageitems)
        page_data = paginator.paginate_queryset(posts, request)
        serializer = UserSerializer(page_data, many=True)
        return paginator.get_paginated_response(serializer.data)
