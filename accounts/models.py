from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.models import Permission, Group

from django.conf import settings
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone_number=None, address=None, password=None, is_active=True, is_staff=False, is_admin=False, is_suplier=False, is_manufacturer=False):
        if not email:
            raise ValueError("User Must have email address")
        if not username:
            raise ValueError("User Must have Username")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
            phone_number=phone_number,
        )
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.is_active = is_active
        user.is_suplier = is_suplier
        user.is_manufacturer = is_manufacturer
        user.save(using=self._db)
        return user

    def create_supplier_user(self, first_name, last_name, username, email, phone_number, password=None):
        user = self.create_user(
            first_name,
            last_name,
            username,
            email,
            phone_number,
            password=password,
            is_staff=True,
            is_suplier=True
        )
        return user

    def create_manufacture_user(self, first_name, last_name, username, email, phone_number, password=None):
        user = self.create_user(
            first_name,
            last_name,
            username,
            email,
            phone_number,
            password=password,
            is_staff=True,
            is_manufacturer=True
        )
        return user

    def create_staffuser(self, first_name, last_name, username, email, phone_number, password=None):
        user = self.create_user(
            first_name,
            last_name,
            username,
            email,
            phone_number,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, first_name, last_name, username, email, phone_number, password=None):
        user = self.create_user(
            first_name,
            last_name,
            username,
            email,
            phone_number,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=255, verbose_name="First Name")
    last_name = models.CharField(max_length=255, verbose_name="Last Name")
    username = models.CharField(
        max_length=255, unique=True, verbose_name="User Name")
    email = models.EmailField(
        verbose_name="Email Address",
        max_length=255,
        unique=True
    )
    phone_number = models.CharField(
        max_length=20, unique=True, verbose_name="Phone Number")
    is_active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=False)  # staff user non superuser
    admin = models.BooleanField(default=False)  # superuser
    is_suplier = models.BooleanField(
        default=False)  # if user is supplier admin
    is_manufacturer = models.BooleanField(
        default=False)  # if user is manufacturer admin
    group_name = models.ForeignKey(Group,on_delete=models.CASCADE,verbose_name="Group",null=True,blank=True)
    created_by_admin_id = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'phone_number']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return "@{}.".format(self.username)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class ProfileImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    profile_image = models.ImageField()



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
