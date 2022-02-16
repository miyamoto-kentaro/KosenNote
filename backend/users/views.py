

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import tree

from rest_framework import status
from rest_framework import authentication
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView

from .models import PreRegister
from .serializers import UserSerializer, PreRegisterSerializer

User = get_user_model()


class CreatePreRegister(APIView):
    def exist_object(self, email):
        preregister = PreRegister.objects.get(email=email)
        if preregister:
            preregister.delete()


    def post(self, request):
        self.exist_object(request.data['email'])
        # print(request)
        serializer = PreRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

