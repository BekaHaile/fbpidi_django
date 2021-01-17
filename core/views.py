from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.exceptions import ObjectDoesNotExist

# 
from admin_site import models
from admin_site.forms import SubCategoryForm,ProductCreationForm
from accounts.models import User,Company,Customer
from accounts.forms import CompanyForm
from social_django.context_processors import REDIRECT_FIELD_NAME, login_redirect


class IndexView(View):
    def get(self,*args,**kwargs):
    
        products = models.Product.objects.all()
        category = models.Category.objects.all()
        sub_category = models.SubCategory.objects.all()
        company = Company.objects.all()
        context = {'products':products,'category':category,'sub_c1ategory':sub_category,'companies':company}
        return render(self.request,"frontpages/index.html",context)

class ProfileView(LoginRequiredMixin, View):
    def get(self,*args,**kwargs):
        context = {}
        user_detail = Customer.objects.get(user=self.request.user)
        context = {'user_detail':user_detail}
        return render(self.request,"frontpages/mydash.html",context)

    def post(self,*args,**kwargs):
        user_detail = Customer.objects.get(user=self.request.user)
        user = User.objects.get(id=self.request.user.id)
        
        if self.request.POST['first_name'] != None:
            user.first_name = self.request.POST['first_name']
        if self.request.POST['last_name'] != None:
            user.last_name = self.request.POST['last_name']
        if self.request.POST['phone_number'] != None:
            user.phone_number = self.request.POST['phone_number']
        if self.request.FILES.get('profile_image') != None:
            user.profile_image = self.request.FILES.get('profile_image')
        user.save()
        if self.request.POST['address'] != None:
            user_detail.address = self.request.POST['address']
        if self.request.POST['city'] != None:
            user_detail.city = self.request.POST['city']
        if self.request.POST['postal_code'] != None:
            user_detail.postal_code = self.request.POST['postal_code']
        if self.request.POST['country'] != None:
            user_detail.country = self.request.POST['country']
        if self.request.POST['facebook_link'] != None:
            user_detail.facebook_link = self.request.POST['facebook_link']
        if self.request.POST['google_link'] != None:
            user_detail.google_link = self.request.POST['google_link']
        if self.request.POST['twitter_link'] != None:
            user_detail.twiter_link = self.request.POST['twitter_link']
        if self.request.POST['pinterest_link'] != None:
            user_detail.pintrest_link = self.request.POST['pinterest_link']
        if self.request.POST['bio'] != None:
            user_detail.bio = self.request.POST['bio']
        user_detail.save()
        return redirect("mydash")
         