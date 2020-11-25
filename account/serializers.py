from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Owner
from rest_framework.authtoken.models import Token

# user serializer class
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required':True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# owner serializer class
class OwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Owner
        fields = '__all__'

