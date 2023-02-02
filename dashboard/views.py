from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import get_user_model
from accounts.models import User
from rest_framework.response import Response
from .serializers import ProfileSerializer, PostSerializer, CatalogueSerializer, DirectMessageSerializer
from rest_framework.views import APIView
from django.http.response import JsonResponse

from rest_framework import viewsets
from rest_framework import generics
from .models import Post, Catalogue, Profile
from .permissions import TokenBackend
from django.core.exceptions import ValidationError


User = get_user_model()
# Create your views here.

class ProfileView(APIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (TokenBackend,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}
        serializer.is_valid(raise_exception=True)
        profile = serializer.save(user=request.user)
        data['response'] = 'successfully created a profile.'
        data['name'] = profile.name
        data['location'] = profile.location
        return Response(data)

    def get(self, request):
        try:
            user = Profile.objects.all().filter(user=request.user)
            
        except Profile.DoesNotExist:
            return Response({"message": "user profile does not exist, kindly create a new profile"})
        serializer = ProfileSerializer(user, many=True)
        
        return Response(serializer.data)

    def put(self, request):
        try:
            instance = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return JsonResponse({'error': 'profile not found'}, status=404)

        serializer = ProfileSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request):
        try:
            user = Profile.objects.get(user=request.user)
            user.delete()
            return Response({"message": "user profile successfully deleted"})
        except Profile.DoesNotExist:
            return Response({"message": "User does not exist"})
        


        
class PostCreateView(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (TokenBackend,)
   
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save(author=request.user)
                data = {}
                data['response'] = 'successfully created a post'
                data['data'] = serializer.data
                return Response(data)
            except ValidationError:
                return Response({"message": "validation error!!"})

    def get(self, request):
        all_post = Post.objects.all().filter(author=request.user)
        serializer = PostSerializer(all_post, many=True)
        return Response(serializer.data)
class Update(APIView):
    def put(self, request, pk):
        try:
            instance = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'post not found'}, status=404)

        serializer = PostSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    def delete(self, request, pk):
        try:
            instance = Post.objects.get(id=pk)
            instance.delete()
            return Response({"message": "post successfully deleted"}, 200)
        except Post.DoesNotExist:
            return Response({"message": "post id does not exist!"}, 404)
    



class CatalogueView(APIView):
    queryset = Catalogue.objects.all()
    serializer_class = CatalogueSerializer
    permission_classes = (TokenBackend,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save(owner=request.user)
                data = {}
                data['response'] = 'successfully created a catalogue'
                data['data'] = serializer.data
                return Response(data)
            except ValidationError:
                return Response({"message": "validation error!!"})

    def get(self, request):
        all_products = Catalogue.objects.all().filter(owner=request.user)
        serializer = CatalogueSerializer(all_products, many=True)
        return Response(serializer.data)

class CatalogueUpdate(APIView):
    def put(self, request, pk):
        try:
            instance = Catalogue.objects.get(id=pk)
        except Catalogue.DoesNotExist:
            return JsonResponse({'error': 'product not found'}, status=404)

        serializer = CatalogueSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    def delete(self, request, pk):
        try:
            instance = Catalogue.objects.get(id=pk)
            instance.delete()
            return Response({"message": "product successfully deleted"}, 200)
        except Catalogue.DoesNotExist:
            return Response({"message": "product id does not exist!"}, 404)






# from rest_framework.generics import ListAPIView
# from rest_framework.response import Response
# from .models import MyModel
# from .serializers import MyModelSerializer

# class MyListView(ListAPIView):
#     queryset = MyModel.objects.all()
#     serializer_class = MyModelSerializer

#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)


# @api_view(["GET"])
# @authentication_classes([TokenBackend])
# @permission_classes([IsUser])
# def catalogueview(request):
#     if request.method == "GET":
#         auth_class = TokenBackend.auth(request)
#         user = auth_class.user
#     x = TokenBackend.auth(request)
#     return Response({"message": "working"})





# from rest_framework import permissions
# from .models import Clients
# import requests
# import json
# class IsAuthenticated(APIView):
#     def post(self, request):
#         header = request.headers.get('Authorization')
#         if header is None:
#             return None
#         token = header.split()[1]
#         url = 'http://18.207.205.10/auth/auth/verify'
#         headers = {
#                     "Content-Type": "application/json",
#                     "Authorization": f"Bearer {token}"
#                 } 

#         response = requests.post(url=url, headers=headers)
#         status = response.status_code

#         # return Response(response)

#         if status == 200:
#             return Response(True)

#         else:
#             return Response({'message': 'verification failed'}, 400)



#         # return request.user.is_authenticated and request.user.is_active
