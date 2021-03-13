from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser
)
from django.contrib.auth.models import User, Permission, Group
from django.conf import settings
from django.db.models.signals import post_save
from company.models import Company, CompanyStaff

#imports for authToken (the authentication for the rest api part), to generate tokens automatically
# from django.conf import settings
#from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token 

# the method for generating tokens while users are created (not used for already created users)
@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)
        

class UserProfile(AbstractUser):
    phone_number = models.CharField(max_length=20,blank=True,null=True) 
    is_customer = models.BooleanField(default=False)  # ifFbpidiUser is customer
    is_company_admin = models.BooleanField(default=False)  # ifFbpidiUser is company admin
    is_company_staff = models.BooleanField(default=False) # ifFbpidiUser is company staff
    profile_image = models.ImageField(blank=True)
    created_by = models.ForeignKey('self',on_delete=models.RESTRICT,null=True,blank=True,related_name="user_created_by")
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    last_updated_by = models.ForeignKey('self',on_delete=models.RESTRICT,null=True,blank=True,related_name="updated_by_user")
    last_updated_date = models.DateTimeField(null=True)
    expired = models.BooleanField(default=False)

    class Meta(AbstractUser.Meta):
        ordering=('-created_date',)

    def get_company_name(self):
        return self.get_company().name if self.is_staff else None
        # if self.is_company_admin:
        #    return CompanyAdmin.objects.get(user = self).get_company_name()
        # elif self.is_company_staff:
        #     return CompanyStaff.objects.get(user = self).get_company_name()

    def get_company(self):
        try:
            if self.is_company_admin:
                return Company.objects.get(contact_person = self)
            elif self.is_company_staff:
                return Company.objects.get(company_staff = self)
            elif self.is_superuser:
                return Company.objects.get(name="FBPIDI")
        except Company.DoesNotExist:
            return None


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=100,default="")
    city = models.CharField(max_length=100,default="")
    postal_code = models.CharField(max_length=100,default="")
    country = models.CharField(max_length=100,default="")
    facebook_link = models.CharField(max_length=100,default="")
    twiter_link = models.CharField(max_length=100,default="")
    google_link = models.CharField(max_length=100,default="")
    pintrest_link = models.CharField(max_length=100,default="")
    bio = models.TextField()
    profile_image = models.ImageField(default="")
    time_stamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.user.username

    def get_year(self):
        return self.time_stamp.year


class CompanyAdmin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    designation = models.CharField(max_length=200,null=True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    #this method works fine for only the company admin that created the company object (how to )
    # def get_company_name(self):
    #     return Company.objects.get(user = self.user).company_name if Company.objects.get(user = self.user).company_name else None

    # def get_company(self):
    #     return Company.objects.get(user = self.user) if Company.objects.get(user = self.user) else None