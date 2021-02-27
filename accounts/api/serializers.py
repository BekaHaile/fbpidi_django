from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate

from django.contrib.auth.models import Group, Permission
from accounts.models import User, CompanyAdmin, CompanyStaff, Customer
from django.db import transaction

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name','last_name', 'email', 'password', 
                    'password2', 'phone_number', 'profile_image',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(email=validated_data['email'],  username=validated_data['username'],
                    first_name=validated_data['first_name'], last_name=validated_data['last_name'],
                    phone_number=validated_data['phone_number'], profile_image=validated_data['profile_image'])
        
        if validated_data['password'] != validated_data['password2']:
            raise serializers.ValidationError({'password': 'Password1 and Password2 must mutch!!'})
        
        user.set_password(validated_data['password'])
        user.save()#####
        return user


class CompanyAdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False) 
    class Meta:
        model = CompanyAdmin
        fields = ('user','is_suplier', 'is_manufacturer' )


class CustomerCreationSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False) 
    class Meta:
        model = Customer
        fields = ('user',)
        

    @transaction.atomic
    def save(self, user):
        user = user
        user.is_staff = False
        user.is_superuser = False
        user.is_customer = True
        user.is_company_admin = False
        user.is_active = True
        user.save()
        
        customer = Customer.objects.create(user = user)
        customer.save()
        return customer


class CustomerDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False, read_only=True)
    profile_image = serializers.ImageField(required=False, )
    class Meta:
        model = Customer
        fields = "__all__"


class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token and provider.
    """
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)







