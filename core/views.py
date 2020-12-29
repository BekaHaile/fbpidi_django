from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# 
from core import models
from core.forms import SubCategoryForm,ProductCreationForm
from accounts.models import User,Company
from accounts.forms import CompanyForm


# category related views

# This is class/view is crated for displaying all categories and sub categories
class CategoryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = {}
        if self.kwargs['option'] == 'category':
            categories = models.Category.objects.all()
            context = {'categories':categories,'option':'category'}
        elif self.kwargs['option'] == 'sub_category':
            sub_categories = models.SubCategory.objects.all()
            context = {
                "sub_categories":sub_categories,'option':'sub_category'
            }
        return render(self.request,"admin/pages/categories.html",context)

# This class/view is created for displaying category and sub category detail and editing
class CategoryDetail(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = {}
        if self.kwargs['option'] == "category":
            category = models.Category.objects.get(id=self.kwargs['cat_id'])
            context = {
                'category':category,
                'edit':'edit'
            }
        elif self.kwargs['option'] == "sub_category":
            sub_category = models.SubCategory.objects.get(id=self.kwargs['cat_id'])
            cat_types = models.Category.objects.all().distinct('category_name')
            context = {
                'sub_category':sub_category,
                'categories_name':cat_types,
                'edit':'edit'
            }
        return render(self.request,"admin/pages/category_form.html",context)
    
    def post(self,*args,**kwargs):
        context = {}
        message = ""
        option = ""
        if self.kwargs['option'] == "category":
            category = models.Category.objects.get(id=self.kwargs['cat_id'])
            category.category_name = self.request.POST['category_name']
            category.category_type = self.request.POST['category_type']
            category.description = self.request.POST['description']
            category.category_name_am = self.request.POST['category_name_am']
            category.category_type_am = self.request.POST['category_type']
            category.description_am = self.request.POST['description_am']
            category.save()
            message = "Category Updated Successfully"
            option = "category"
        elif self.kwargs['option'] == "sub_category":
            sub_category = models.SubCategory.objects.get(id=self.kwargs['cat_id'])
            sub_category.category_name = models.Category.objects.get(id=self.request.POST['category_name'])
            sub_category.sub_category_name = self.request.POST['sub_category_name']
            sub_category.description = self.request.POST['description']
            sub_category.sub_category_name_am = self.request.POST['sub_category_name_am']
            sub_category.description_am = self.request.POST['description_am']
            sub_category.save()
            message = "Sub-Category Updated Successfully"
            option = "sub_category"
        messages.success(self.request,message)
        return redirect("p_categories",option=option)

# This class/view is created for creating new categories
class CreateCategories(LoginRequiredMixin,View):
    cat_list_am = { "Food":'ምግብ',"Beverage":'መጠጥ',"pharmaceuticals":'መድሃኒት' }
     
    def get(self,*args,**kwargs):
        context = {}
        if self.kwargs['option'] == "category":
            context = {
                'category':"category"
            }
        elif self.kwargs['option'] == "sub_category":
            form = SubCategoryForm()
            context = {
                'sub_category':'sub_category',
                'form':form,
            }
        return render(self.request,"admin/pages/category_form.html",context)
    
    def post(self,*args,**kwargs):
        if self.kwargs['option'] == "category":
            category = models.Category(
                user=self.request.user,
                category_name=self.request.POST['category_name'],
                category_type=self.request.POST['category_type'],
                description=self.request.POST['description'],
                category_name_am=self.request.POST['category_name_am'],
                category_type_am=self.cat_list_am[self.request.POST['category_type']],
                description_am=self.request.POST['description_am']
            ) 
            category.save()
            messages.success(self.request,"You Created a New Category")
            return redirect("p_categories",option='category')
        elif self.kwargs['option'] == "sub_category":
            form = SubCategoryForm(self.request.POST)
            if form.is_valid():
                sub_category = models.SubCategory(
                    user=self.request.user,
                    category_name=form.cleaned_data.get('category_name'),
                    sub_category_name=form.cleaned_data.get('sub_category_name'),
                    description=form.cleaned_data.get('description'),
                    sub_category_name_am=form.cleaned_data.get('sub_category_name_am'),
                    description_am=form.cleaned_data.get('description_am')
                )
                sub_category.save()
                messages.success(self.request,"You Created a New Sub Category")
                return redirect("p_categories", option='sub_category')

def create_company_after_signup_view(request,id):
    if request.method == "POST":
        form = CompanyForm(request.POST,request.FILES)
        user = User.objects.get(id=id)
        company_type = ""
        if user.is_suplier:
            company_type = "supplier"
            company_type_am = "አቅራቢ"
        elif user.is_manufacturer:
            company_type = "manufacturer"
            company_type_am = "አምራች"
        if form.is_valid():
            company_info = Company(
                user=user,
                company_name=form.cleaned_data.get("company_name"),
                company_name_am=form.cleaned_data.get("company_name_am"),
                email=form.cleaned_data.get("email"),
                phone_number=form.cleaned_data.get("phone_number"),
                company_type=company_type,
                company_type_am = company_type_am,
                location=form.cleaned_data.get('location'),
                company_logo=form.cleaned_data.get("company_logo"),
                company_intro=form.cleaned_data.get("company_intro"),
                detail=form.cleaned_data.get("detail"),
                detail_am=form.cleaned_data.get("detail_am")
            )
            company_info.save()
            return redirect("admin:login")
        else:
            return render(request,"admin/pages/company_form.html",{'form':form,'comp_user':user})
    else:
        form = CompanyForm()
        comp_user = User.objects.get(id=id)
        context = {'form':form,'comp_user':comp_user}
        return render(request,"admin/pages/company_form.html",context)
          
        

# company related view
class CreateCompanyProfileView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        form = CompanyForm()
        context = {}
        if self.kwargs['option'] == 'view':
            company_detail = Company.objects.get(user=self.request.user)
            context={'company':company_detail}
            return render(self.request,"admin/pages/company_detail.html",context)
        elif self.kwargs['option'] == 'edit':
            company_detail = Company.objects.get(id=self.kwargs['id'])
            context={'company':company_detail,'edit':'edit'}
            return render(self.request,"admin/pages/company_profile.html",context)
        elif self.kwargs['option'] == 'create':
            context = {'form':form}
            return render(self.request,"admin/pages/company_profile.html",context)
        elif self.kwargs['option'] == "create_now":
            comp_user = User.objects.get(id=self.kwargs['id'])
            context = {'form':form,'comp_user':comp_user}
            return render(self.request,"admin/pages/company_form.html",context)
            
        
    
    def post(self,*args,**kwargs):
        company_type = ""
        if self.request.user.is_suplier:
            company_type = "supplier"
        elif self.request.user.is_manufacturer:
            company_type = "manufacturer"
        elif self.request.user.admin:
            company_type = self.request.POST['company_type']

        if self.kwargs['option'] == 'create':
            form = CompanyForm(self.request.POST,self.request.FILES)
            if form.is_valid():
                if self.request.user.is_admin:
                    company_info,created = Company.objects.get_or_create(user=self.request.user)
                    company_info.company_name=form.cleaned_data.get("company_name")
                    company_info.company_name_am=form.cleaned_data.get("company_name_am")
                    company_info.email=form.cleaned_data.get("email")
                    company_info.phone_number=form.cleaned_data.get("phone_number")
                    company_info.company_type=company_type
                    company_info.location=form.cleaned_data.get('location')
                    company_info.company_logo=form.cleaned_data.get("company_logo")
                    company_info.company_intro=form.cleaned_data.get("company_intro")
                    company_info.detail=form.cleaned_data.get("detail")
                    company_info.detail_am=form.cleaned_data.get("detail_am")
                    company_info.save()
                else:
                    company_info = Company(
                        user=self.request.user,
                        company_name=form.cleaned_data.get("company_name"),
                        company_name_am=form.cleaned_data.get("company_name_am"),
                        email=form.cleaned_data.get("email"),
                        phone_number=form.cleaned_data.get("phone_number"),
                        company_type=company_type,
                        location=form.cleaned_data.get('location'),
                        company_logo=form.cleaned_data.get("company_logo"),
                        company_intro=form.cleaned_data.get("company_intro"),
                        detail=form.cleaned_data.get("detail"),
                        detail_am = form.cleaned_data.get("detail_am"),
                    )
                    company_info.save()
                messages.success(self.request,"Company Profile Created")
                return redirect("comp_profile",option="view",id=company_info.id)
        elif self.kwargs['option'] == 'edit':
            print(self.request.POST.get("company_name"))
            company_info = Company.objects.get(id=self.request.POST['comp_id'])
            company_info.company_name=self.request.POST['company_name']
            company_info.company_name_am=self.request.POST['company_name_am']
            company_info.email=self.request.POST['email']
            company_info.phone_number=self.request.POST['phone_number']
            company_info.location=self.request.POST['location']
            if self.request.FILES.get('company_logo') == None:
                pass
            elif self.request.FILES.get('company_logo') != None:
                company_info.company_logo=self.request.FILES.get('company_logo')
            if self.request.FILES.get("company_intro") == None:
                pass
            elif self.request.FILES.get("company_intro") != None:
                company_info.company_intro=self.request.FILES.get("company_intro")
            company_info.detail=self.request.POST["detail"]
            company_info.detail_am=self.request.POST["detail_am"]
            company_info.save()
            messages.success(self.request,"Company Profile Created")
            return redirect("comp_profile",option="view",id=company_info.id)


class CompaniesView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = {}
        if self.kwargs['option'] == "supplier":
            suppliers = Company.objects.filter(company_type="supplier")
            context = {
                'companies':suppliers
            }
        elif self.kwargs['option'] == "manufacturer":
            manufacturers = Company.objects.filter(company_type="manufacturer")
            context = {
                'companies':manufacturers
            }
        print(context)
        return render(self.request,"admin/pages/companies.html",context)

class CompaniesDetailView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        company = ""
        context = {}
        try:
            company = Company.objects.get(id=self.kwargs['id'])
            context = {
                'company':company
            }
        except ObjectDoesNotExist:
            messages.warning(self.request,"Company does not Exist")
            return redirect("companies")
        return render(self.request,"admin/pages/company_detail.html",context)


class AdminProductListView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        products = ""
        if self.kwargs['user_type'] == 'admin':
            products = models.Product.objects.all()
            company = Company.objects.all()
            context = {'products':products,'companies':company}
        elif self.kwargs['user_type'] == 'provider':
            products = models.Product.objects.filter(user=self.request.user)
            company = Company.objects.filter(user=self.request.user)
            context = {'products':products,'companies':company}
        else:
            company = Company.objects.get(id=self.kwargs['user_type'])
            products = models.Product.objects.filter(user=company.user)
            context = {'products':products,'company':company}
        return render(self.request,"admin/pages/product_list.html",context)

class ProductDetailView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        product = get_object_or_404(models.Product,id=self.kwargs['id'])
        company = ""
        try:
            company = Company.objects.get(user=product.user)
        except ObjectDoesNotExist:
            company = None
        product_image = models.ProductImage.objects.filter(product=product)
        product_price = models.ProductPrice.objects.filter(product=product)
        if self.kwargs['option'] == 'edit':
            pcats = models.SubCategory.objects.all().exclude(id=product.category.id)
            return render(self.request,"admin/pages/product_form.html",{'product':product,'pcats':pcats,'company':company,'edit':'edit'})    
        elif self.kwargs['option'] == 'view':
            return render(self.request,"admin/pages/product_detail.html",{'product':product,'company':company,'product_imgs':product_image,'product_price':product_price})

    def post(self,*args,**kwargs):
        product = models.Product.objects.get(id=self.kwargs['id'])
        if self.kwargs['option'] == 'edit_all':
            category = models.SubCategory.objects.get(id=self.request.POST['category'])
            product.name=self.request.POST['name']
            product.name_am = self.request.POST['name_am']
            product.category=category
            product.description = self.request.POST['description']
            product.description_am = self.request.POST['description_am']
            if self.request.FILES.get('image') == None:
                pass
            elif self.request.FILES.get('image') != None:
                product.image = self.request.FILES.get('image')
            product.save()
            messages.success(self.request,"Successfully Edited Product")
            return redirect("product_detail",id=product.id,option='view')
        else:
            product.description = self.request.POST['description']
            product.save()
            messages.success(self.request,"Successfully Edited Product")
            return redirect("product_detail",id=product.id,option='view')

class AddProductImage(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        item = self.request.POST['product']
        image = self.request.FILES['image']
        product = models.Product.objects.get(id=item)
        product_image = models.ProductImage(
            product=product,image=image
        )
        product_image.save()
        messages.success(self.request,"Image Added Successfully!")
        return redirect("product_detail",id=product.id,option='view')

class CreateProductView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        form = ProductCreationForm()
        context = {'form':form}
        return render(self.request,'admin/pages/product_form.html',context)
    
    def post(self,*args,**kwargs):
        form = ProductCreationForm(self.request.POST,self.request.FILES)
        if form.is_valid():
            product = models.Product(
                user=self.request.user,
                name=form.cleaned_data.get('name'),
                name_am=form.cleaned_data.get('name_am'),
                category=form.cleaned_data.get('category'),
                description=form.cleaned_data.get("description"),
                description_am=form.cleaned_data.get('description_am'),
                image=form.cleaned_data.get("image")
            )
            product.save()
            messages.success(self.request,"Product Created Successfully!")
            return redirect("admin:index")

class CreatePrice(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        pid = self.request.POST['product']
        price = self.request.POST['price']
        start_date = self.request.POST['start_date']
        end_date = self.request.POST['end_date']
        product = models.Product.objects.get(id=pid)
        if self.request.POST['option'] == 'change':
            old_price = models.ProductPrice.objects.get(id=self.request.POST['priceid'])
            old_price.price = float(price)
            old_price.save()
        elif self.request.POST['option'] == 'new':
            price_obj = models.ProductPrice(
                user=self.request.user,
                product=product,
                price=float(price)
            )
            price_obj.save()
        messages.success(self.request,"Price Added Successfully!")
        return redirect("product_detail", id=product.id,option='view')


class DeleteView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        message = ""
        if self.kwargs['model_name'] == 'category':
            category = models.Category.objects.get(id=self.kwargs['id'])
            category.delete()
            message = "Category Deleted"
            messages.success(self.request,message)
            return redirect("p_categories",option='category')
        elif self.kwargs['model_name'] == 'sub_category':
            sub_category = models.SubCategory.objects.get(id=self.kwargs['id'])
            sub_category.delete()
            message ="Sub-Category Deleted"
            messages.success(self.request,message)
            return redirect("p_categories",option='sub_category')
        elif self.kwargs['model_name'] == 'user_account':
            user = User.objects.get(id=self.kwargs['id'])
            user.delete()
            message ="User Deleted"
            messages.success(self.request,message)
            return redirect("users_list")
        elif self.kwargs['model_name'] == 'product':
            product = models.Product.objects.get(id=self.kwargs['id'])
            product.delete()
            message ="Product Deleted"
            messages.success(self.request,message)
            return redirect("admin:index")
        elif self.kwargs['model_name'] == 'company':
            company = Company.objects.get(id=self.kwargs['id'])
            company.delete()
            message ="Company Deleted"
            messages.success(self.request,message)
            return redirect("admin:index")
        elif self.kwargs['model_name'] == 'product_image':
            pdimage = models.ProductImage.objects.get(id=self.kwargs['id'])
            pdimage.delete()
            message ="Image Deleted"
            messages.success(self.request,message)
            return redirect("product_detail",id=pdimage.product.id,option='view')
        