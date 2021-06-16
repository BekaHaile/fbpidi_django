from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
# 
from product.models import *
from admin_site.models import Category
from admin_site.views.views import record_visit
from company.models import Company,CompanyLike
# 
from accounts.models import UserProfile,Company,Customer
from product.forms import ReviewForm
#
from collaborations.models import News, NewsImages



class IndexView(View):
    def get(self,*args,**kwargs):
        record_visit(self.request)
        products = Product.objects.filter(is_active = True)
        category = Category.objects.all()
        sub_category = SubCategory.objects.all()
        company = Company.objects.filter(is_active=True).exclude(main_category="FBPIDI")
        #12345 make it filter the latest 4 or 5
        news_list = News.objects.all()[:9]
        collaboration_modules = ['Announcement','Blog','Event','Forum', 'News','Polls','Research','Tender','Vacancy']
        context = {'products':products,'categories':category,'sub_categories':sub_category,'companies':company, 'news_list':news_list, 'NEWS_CATAGORY': News.NEWS_CATAGORY, 'modules':collaboration_modules}
      
        return render(self.request,"frontpages/index.html",context)


class ProfileView(LoginRequiredMixin, View):
    def get(self,*args,**kwargs):
        context = {}
        user_detail = Customer.objects.get(user=self.request.user)
        context = {'user_detail':user_detail}
        return render(self.request,"frontpages/profile/mydash.html",context)

    def post(self,*args,**kwargs):
        user_detail = Customer.objects.get(user=self.request.user)
        user = UserProfile.objects.get(id=self.request.user.id)

        
        if self.request.POST['first_name'] != None:
            user.first_name = self.request.POST['first_name']
        if self.request.POST['last_name'] != None:
            user.last_name = self.request.POST['last_name']
        if self.request.POST['phone_number'] != None:
            user.phone_number = self.request.POST['phone_number']
        if self.request.FILES.get('profile_image') != None:
            user.profile_image = self.request.FILES.get('profile_image')
            #12345 two profile images for a single customer user
            user_detail.profile_image = self.request.FILES.get('profile_image')
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

class MyFavorite(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = {}
        try:
            likes_product = ProductLike.objects.filter(user=self.request.user)
            # paginator = Paginator(likes_product, 5) 

            # page_number = request.GET.get('page')
            # page_obj = paginator.get_page(page_number)
            context['liked_products'] = likes_product
        except Exception:
            context = {}
        return render(self.request,"frontpages/profile/myfavorite.html",context)

class MyOrders(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = {}
        try:
            context['orders'] = ProductInquiry.objects.filter(user=self.request.user)
        except Exception:
            print("@@@ Exception at My Orders, ",e)
            return redirect('/')
        print(context)
        return render(self.request,"frontpages/profile/orders.html",context)