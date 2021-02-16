from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

# 
from product.models import Product, ProductImage,Review
from admin_site.models import Category,SubCategory
from company.models import Company
# 
from accounts.models import User,Company,Customer
from accounts.forms import CompanyForm
from product.forms import ReviewForm
#
from collaborations.models import News, NewsImages


class IndexView(View):
    def get(self,*args,**kwargs):
    
        products = Product.objects.all()
        category = Category.objects.all()
        sub_category = SubCategory.objects.all()
        company = Company.objects.all()
        #??make it filter the latest 4 or 5
        news_list = News.objects.all()

        
        context = {'products':products,'categories':category,'sub_categories':sub_category,'companies':company, 'news_list':news_list, 'NEWS_CATAGORY':News.NEWS_CATAGORY }
        return render(self.request,"frontpages/index.html",context)

class ProductByCategoryView(View):
    def get(self,*args,**kwargs):
        products = Product.objects.filter(category=self.kwargs['cat_id'])
        context = {'products':products,'count':products.count()}
        return render(self.request,"frontpages/product/product_category.html",context)


class ProductByMainCategory(View):
    def get(self,*args,**kwargs):
        products = Product.objects.all()
        product_list = []
        context = {}
        if self.kwargs['option'] == "Beverage":
            for product in products:
                if product.category.category_name.category_type == "Beverage":
                    product_list.append(product)
        elif self.kwargs['option'] == "Food":
            for product in products:
                if product.category.category_name.category_type == "Food":
                    product_list.append(product)
        elif self.kwargs['option'] == "Pharmaceuticals":
            for product in products:
                if product.category.category_name.category_type == "Pharmaceuticals":
                    product_list.append(product)
        elif self.kwargs['option'] == "all":
            for product in products:
                product_list.append(product)
        context['products'] = product_list
        context['count'] = len(product_list)
        return render(self.request,"frontpages/product/product_category.html",context)

class MnfcCompanyByMainCategory(View):
    def get(self,*args,**kwargs):
        companies = Company.objects.filter(company_type="manufacturer")
        company_list = []
        context = {}
        if self.kwargs['option'] == "Beverage":
            for company in companies:
                if company.product_category.category_name.category_type == "Beverage":
                    company_list.append(company)
        elif self.kwargs['option'] == "Food":
            for company in companies:
                if company.product_category.category_name.category_type == "Food":
                    company_list.append(company)
        elif self.kwargs['option'] == "Pharmaceuticals":
            for company in companies:
                if company.product_category.category_name.category_type == "Pharmaceuticals":
                    company_list.append(company)
        elif self.kwargs['option'] == "all":
            for company in companies:
                company_list.append(company)
        context['companies'] = company_list
        context['count'] = len(company_list)
        return render(self.request,"frontpages/company/company_list.html",context)

class SupCompanyByMainCategory(View):
    def get(self,*args,**kwargs):
        companies = Company.objects.filter(company_type="supplier")
        company_list = []
        context = {}
        if self.kwargs['option'] == "Beverage":
            for company in companies:
                if company.product_category.category_name.category_type == "Beverage":
                    company_list.append(company)
        elif self.kwargs['option'] == "Food":
            for company in companies:
                if company.product_category.category_name.category_type == "Food":
                    company_list.append(company)
        elif self.kwargs['option'] == "Pharmaceuticals":
            for company in companies:
                if company.product_category.category_name.category_type == "Pharmaceuticals":
                    company_list.append(company)
        elif self.kwargs['option'] == "all":
            for company in companies:
                company_list.append(company)
        context['companies'] = company_list
        context['count'] = len(company_list)
        return render(self.request,"frontpages/company/company_list.html",context)


class ProductDetailView(View):
    def get(self,*args,**kwargs):
        try:
            form = ReviewForm()
            product = Product.objects.get(id=self.kwargs['id'])
            reviews = Review.objects.filter(product=product)
            images = ProductImage.objects.filter(product=product)
            context = {'product':product,'images':images,'form':form,'reviews':reviews}
            return render(self.request,'frontpages/product/product_detail.html',context)
        except ObjectDoesNotExist:
            return redirect("index")
    
    def post(self, *args,**kwargs):
        form = ReviewForm(self.request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = Product.objects.get(id=self.kwargs['id'])
            review.save()
            return redirect('product_detail',id=self.kwargs['id'])
        else:
            return redirect("product_detail",id=self.kwargs['id'])

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
         