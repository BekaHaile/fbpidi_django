from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser
)
from django.contrib.auth.models import Permission, Group

from django.conf import settings
from django.db.models.signals import post_save


class User(AbstractUser):
    phone_number = models.CharField(max_length=20,blank=True,null=True)
    is_customer = models.BooleanField(default=False)  # if user is customer
    is_company_admin = models.BooleanField(default=False)  # if user is company admin
    is_company_staff = models.BooleanField(default=False) # if user is company staff
    profile_image = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=100,default="")
    city = models.CharField(max_length=100,default="")
    postal_code = models.CharField(max_length=100,default="")
    country = models.CharField(max_length=100,default="")
    facebook_link = models.CharField(max_length=100,default="")
    twiter_link = models.CharField(max_length=100,default="")
    google_link = models.CharField(max_length=100,default="")
    pintrest_link = models.CharField(max_length=100,default="")
    bio = models.TextField()
    profile_image = models.ImageField()
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class CompanyAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_suplier = models.BooleanField(default=False) # if the user is from a suplier company.
    is_manufacturer = models.BooleanField(default=False) # if the user is from a manufacturer company.
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class CompanyStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company = models.ForeignKey('Company',on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Company(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    company_name = models.CharField(
        max_length=200, verbose_name="Company Name(English)")
    company_name_am = models.CharField(
        max_length=200, verbose_name="Company Name(Amharic)")
    location = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=20)
    detail = models.TextField(verbose_name="Company Detail(English)")
    detail_am = models.TextField(verbose_name="Company Detail(Amharic)")
    company_logo = models.ImageField()
    company_intro = models.FileField()
    company_type = models.CharField(max_length=255)
    company_type_am = models.CharField(max_length=255,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


class AssignedRoles(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    roles = models.ForeignKey(Permission, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.roles.codename
