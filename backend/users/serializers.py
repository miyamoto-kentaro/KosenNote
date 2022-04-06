import uuid

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import PreRegister

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username','email','password']
    # <Your other UserSerializer stuff here>

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class PreRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = PreRegister
        fields = ['id', 'email']
        # read_only_fields = ('created_at')
    
    def create(self, validated_data):
        random_authentication_code = uuid.uuid4()
        return PreRegister.objects.create(authentication_code=random_authentication_code,**validated_data)
