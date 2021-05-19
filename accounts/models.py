from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser
)
from django.contrib.auth.models import User, Permission, Group
from django.conf import settings
from django.db.models.signals import post_save
from django.core.validators import FileExtensionValidator
from django.dispatch import receiver
from rest_framework.authtoken.models import Token 

from company.models import Company, CompanyStaff

#imports for authToken (the authentication for the rest api part), to generate tokens automatically
# from django.conf import settings
#from django.db.models.signals import post_save

allowed_image_extensions = ['png','jpg','jpeg','webp',]


# the method for generating tokens while users are created (not used for already created users)
@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)
        

class UserProfile(AbstractUser):
    email = models.EmailField(verbose_name="Email Address",unique=True)
    phone_number = models.CharField(max_length=20,blank=True,null=True) 
    is_customer = models.BooleanField(default=False)  # ifFbpidiUser is customer
    is_company_admin = models.BooleanField(default=False)  # ifFbpidiUser is company admin
    is_company_staff = models.BooleanField(default=False) # ifFbpcompanyUser is company staff
    is_fbpidi_staff = models.BooleanField(default=False) # ifFbpidiUser is Fnpidi staff
    profile_image = models.ImageField(blank=True,help_text="Accepted formats: png, jpg, jpeg,webp. Max file size 10 MB",
                    validators=[FileExtensionValidator(allowed_extensions=allowed_image_extensions)])
    created_by = models.ForeignKey('self',on_delete=models.RESTRICT,null=True,blank=True,related_name="user_created_by")
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    last_updated_by = models.ForeignKey('self',on_delete=models.RESTRICT,null=True,blank=True,related_name="updated_by_user")
    last_updated_date = models.DateTimeField(null=True)
    expired = models.BooleanField(default=False)

    

    def __str__(self):
        return "{} : {} {}".format(self.username,self.first_name,self.last_name)

    class Meta(AbstractUser.Meta):
        ordering=('-created_date',)


    def get_company(self):
        try:
            if self.is_company_admin:
                return Company.objects.get(contact_person = self)
            elif self.is_company_staff:
                return CompanyStaff.objects.get(user=self).company
            elif self.is_superuser:
                return Company.objects.get(main_category="FBPIDI")
            elif self.is_fbpidi_staff:
                return Company.objects.get(main_category="FBPIDI")
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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="company_admin")
    designation = models.CharField(max_length=200,null=True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return self.user.username
    
    #this method works fine for only the company admin that created the company object (how to )
    # def get_company_name(self):
    #     return Company.objects.get(user = self.user).company_name if Company.objects.get(user = self.user).company_name else None

    # def get_company(self):
    #     return Company.objects.get(user = self.user) if Company.objects.get(user = self.user) else None


class Subscribers(models.Model):
	# users can subscribe using an email address or their FBPIDI user account
        email = models.EmailField( verbose_name = "Subscriber Email.")
        created_date = models.DateTimeField(auto_now_add = True)
        is_active = models.BooleanField(default =False)

        
	

