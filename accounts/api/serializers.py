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

ADMIN_PERMISSION_LIST = [
    'add_logentry',
    'view_logentry',
    'view_permission',
    'view_group',
    'view_contenttype',
    'view_session',
    'view_category',
    'add_product',
    'change_product',
    'delete_product',
    'view_product',
    'view_subcategory',
    'add_productprice',
    'change_productprice',
    'delete_productprice',
    'view_productprice',
    'add_user',
    'change_user',
    'delete_user',
    'view_user',
    'add_companyadmin',
    'change_companyadmin',
    'delete_companyadmin',
    'view_companyadmin',
    'change_company',
    'delete_company',
    'view_company',
    'add_companystaff',
    'change_companystaff',
    'delete_companystaff',
    'view_companystaff',
    'view_failedloginlog',
    'view_loginlog',
    'view_loginattempt',
    'view_userdeactivation', 

    'add_pollsquestion',
    'view_pollsquestion',
    'change_pollsquestion',
    'delete_pollsquestion',
    'add_choices',
    'view_choices',
    'change_choices',
    'delete_choices',
    
    'view_bank',
    'add_tender',
    'view_tender',
    'change_tender',
    'delete_tender',

    'add_companybankaccount',
    'change_companybankaccount',
    'delete_companybankaccount',
    'view_companybankaccount',
    'view_tenderapplicant',

    'add_news', 
    'view_news', 
    'change_news', 
    'delete_news',

    'add_newsimages', 
    'view_newsimages', 
    'change_newsimages', 
    'delete_newsimages', 

    'add_companyevent', 
    'view_companyevent', 
    'change_companyevent', 
    'delete_companyevent', 
]


class CompanyAdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False) 
    class Meta:
        model = CompanyAdmin
        fields = ('user','is_suplier', 'is_manufacturer' )

    @transaction.atomic
    def save(self, user):
        user = user
        user.is_company_admin = True
        user.is_staff = True
        user.is_superuser = False
        perm_list = []
        for code_name in ADMIN_PERMISSION_LIST:
            
            perm_list.append(Permission.objects.get(codename=code_name))
        user.user_permissions.set(perm_list) 
        user.save()
        
        companyadmin = CompanyAdmin(user = user, is_suplier=self.validated_data['is_suplier'], is_manufacturer=self.validated_data['is_manufacturer'],)
        companyadmin.save()
        return companyadmin


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

