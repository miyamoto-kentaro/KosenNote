import uuid

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import PreRegister

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'locked', 'articles']


class PreRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = PreRegister
        fields = ['id', 'email']
    
    def create(self, validated_data):
        random_authentication_code = uuid.uuid4()
        return PreRegister.objects.create(authentication_code=random_authentication_code,**validated_data)
