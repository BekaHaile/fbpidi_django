import random
import string
import json
import datetime

from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View,ListView,UpdateView,CreateView,DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from django.utils import timezone
from django.http import JsonResponse
from rest_framework import serializers

from django.db.models import Q

from admin_site.models import Category
from product.models import *
from product.forms import *
from company.models import *
from admin_site.decorators import company_created
from admin_site.views.dropdowns import image_cropper
from admin_site.views.views import record_activity

def get_current_year():
    this_year = datetime.datetime.today().year
    return int(this_year-9)



decorators = [never_cache,company_created()]
def create_ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits,k=30))

def create_invoice(invoice,user):
    return '#INV-'.join(random.choices(string.ascii_uppercase + (invoice.join(user.id))))

# This is class/view is crated for displaying all categories and sub categories 
@method_decorator(decorators,name='dispatch')
class CategoryView(LoginRequiredMixin,ListView):
    model = Category
    template_name = "admin/product/categories.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = True
        return context

# This class/view is created for displaying category and sub category detail and editing
@method_decorator(decorators,name='dispatch')
class CategoryDetail(LoginRequiredMixin,UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "admin/product/category_form_update.html"
    success_url = "/admin/categories/"


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = True
        return context

# This class/view is created for creating new categories
@method_decorator(decorators,name='dispatch')
class CreateCategories(LoginRequiredMixin,CreateView):
    cat_list_am = { "Food":'ምግብ',"Beverage":'መጠጥ',"Pharmaceuticals":'መድሃኒት' }
    model = Category
    form_class = CategoryForm
    template_name = "admin/product/category_form_create.html"
    
    def form_valid(self,form):
        category = form.save(commit=False)
        category.created_by = self.request.user
        category.category_type_am=self.cat_list_am[form.cleaned_data.get('category_type')],
        category.save()
        record_activity(self.request.user,"Category","Category data Created",category.id)
        messages.success(self.request,"You Created a New Category")
        return redirect("admin:categories")
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = True
        return context

    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:create_category")

@method_decorator(decorators,name='dispatch')
class SubCategoryView(LoginRequiredMixin,ListView):
    model = SubCategory
    template_name = "admin/product/categories.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return SubCategory.objects.all()
        elif self.request.user.is_company_admin:
            return SubCategory.objects.filter(category_name__in=Company.objects.get(contact_person=self.request.user).category.all())
        elif self.request.user.is_company_staff:
            return SubCategory.objects.filter(category_name__in=CompanyStaff.objects.get(user=self.request.user).company.category.all())
            
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_category'] = True
        return context

# This class/view is created for displaying category and sub category detail and editing
@method_decorator(decorators,name='dispatch')
class SubCategoryDetail(LoginRequiredMixin,UpdateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = "admin/product/category_form_update.html"
    success_url = "/admin/sub_categories/"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_category'] = True
        return context
    
    def form_valid(self,form):        
        sub_category = form.save(commit=False)
        sub_category.created_by = self.request.user
        sub_category.save()
        record_activity(self.request.user,"SubCategory","Sub-Category data Updated",sub_category.id)
        messages.success(self.request,"You Updated a Product Type")
        return redirect("admin:sub_categories")
    
    def form_invalid(self,form):
        message.warning(self.request,form.errors)
        return redirect("admin:edit_subcategory",pk=self.kwargs['pk']) 

# This class/view is created for creating new categories
@method_decorator(decorators,name='dispatch')
class CreateSubCategories(LoginRequiredMixin,CreateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = "admin/product/category_form_create.html"
    

    def form_valid(self,form):        
        sub_category = form.save(commit=False)
        sub_category.created_by = self.request.user
        sub_category.save()
        record_activity(self.request.user,"SubCategory","Sub-Category data Created",sub_category.id)
        messages.success(self.request,"You Created a New Product Type")
        return redirect("admin:sub_categories")
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_category'] = True
        return context
    
    def form_invalid(self,form):
        message.warning(self.request,form.errors)
        return redirect("admin:create_subcategory") 



@method_decorator(decorators,name='dispatch')
class BrandView(LoginRequiredMixin,ListView):
    model = Brand
    template_name = "admin/product/categories.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Brand.objects.all()
        elif self.request.user.is_company_admin:
            return Brand.objects.filter(company=Company.objects.get(contact_person=self.request.user))
        elif self.request.user.is_company_staff:
            return Brand.objects.filter(company=CompanyStaff.objects.get(user=self.request.user).company)
            
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = True
        return context

# This class/view is created for displaying category and sub category detail and editing
@method_decorator(decorators,name='dispatch')
class BrandDetail(LoginRequiredMixin,UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = "admin/product/category_form_update.html"
    success_url = "/admin/brands/"

    def get_form_kwargs(self):
        kwargs = super(BrandDetail,self).get_form_kwargs()
        if self.request.user.is_company_admin:
            kwargs.update({'company': Company.objects.get(contact_person=self.request.user)})
        elif self.request.user.is_company_staff:
            kwargs.update({'company': CompanyStaff.objects.get(user=self.request.user).company})
        return kwargs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = True
        return context

    def form_valid(self,form):        
        brand = form.save(commit=False)
        brand.last_updated_by = self.request.user
        brand.last_updated_date = timezone.now()
        brand.save()
        messages.success(self.request,"You Created a New Brand")
        return redirect("admin:brands")
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:edit_brand",pk=self.kwargs['pk'])

# This class/view is created for creating new brands
@method_decorator(decorators,name='dispatch')
class CreateBrand(LoginRequiredMixin,CreateView):
    model = Brand
    form_class = BrandForm
    template_name = "admin/product/category_form_create.html"
    
    def get_form_kwargs(self):
        kwargs = super(CreateBrand,self).get_form_kwargs()
        if self.request.user.is_company_admin:
            kwargs.update({'company': Company.objects.get(contact_person=self.request.user)})
        elif self.request.user.is_company_staff:
            kwargs.update({'company': CompanyStaff.objects.get(user=self.request.user).company})
        return kwargs

    def form_valid(self,form):        
        brand = form.save(commit=False)
        brand.created_by = self.request.user
        if self.request.user.is_company_admin:
            brand.company = Company.objects.get(contact_person=self.request.user)
        elif self.request.user.is_company_staff:
            brand.company = CompanyStaff.objects.get(user=self.request.user).company
        brand.save()
        messages.success(self.request,"You Created a New Brand")
        return redirect("admin:brands")
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = True
        return context
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:create_brand")


@method_decorator(decorators,name='dispatch')
class AdminProductListView(LoginRequiredMixin,ListView):
    model = Product
    template_name = "admin/product/product_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()
        elif self.request.user.is_company_admin:
            return Product.objects.filter(company=self.request.user.get_company())
        elif self.request.user.is_company_staff:
            return Product.objects.filter(company=CompanyStaff.objects.get(user=self.request.user).company)

@method_decorator(decorators,name='dispatch')
class CreateProductView(LoginRequiredMixin,CreateView):
    model=Product
    form_class = ProductCreationForm
    template_name = "admin/product/product_form.html"

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(CreateProductView,self).get_form_kwargs()
        if self.request.user.is_company_admin:
            kwargs.update({'company': Company.objects.get(contact_person=self.request.user)})
        elif self.request.user.is_company_staff:
            kwargs.update({'company': CompanyStaff.objects.get(user=self.request.user).company})
        return kwargs

    def form_valid(self,form):
        product = form.save(commit=False)
        product.company = self.request.user.get_company()
        product.created_by = self.request.user
        product.save()    
        image_cropper(form.cleaned_data.get('x'),form.cleaned_data.get('y'),
                    form.cleaned_data.get('width'),form.cleaned_data.get('height'),
                    product.image,400,400)
        messages.success(self.request,"Product Created Successfully!")
        return redirect("admin:admin_products")
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return render(self.request,"admin/product/product_form.html",{'form':form})
    

@method_decorator(decorators,name='dispatch')
class ProductUpdateView(LoginRequiredMixin,UpdateView):
    model = Product
    form_class = ProductCreationForm
    template_name = "admin/product/product_form_update.html"

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(ProductUpdateView,self).get_form_kwargs()
        kwargs.update({'company':Product.objects.get(id=self.kwargs['pk']).company})
        return kwargs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = ProductImageForm
        context['price_form'] = ProductPriceForm
        return context
    
    def form_valid(self,form):
        product = form.save(commit=False)
        product.last_updated_by = self.request.user
        product.last_updated_date = timezone.now()
        product.save() 
        image_cropper(form.cleaned_data.get('x'),form.cleaned_data.get('y'),
                    form.cleaned_data.get('width'),form.cleaned_data.get('height'),
                    product.image,400,400)   
        messages.success(self.request,"Product Update Successfully!")
        return redirect("admin:admin_products")
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return render(self.request,"admin/product/product_form_update.html",
                        {'form':form,'image_form':ProductImageForm,'price_form':ProductPriceForm})

@method_decorator(decorators,name='dispatch')
class AddProductImage(LoginRequiredMixin,CreateView):
    model=ProductImage
    form_class = ProductImageForm

    def form_valid(self,form):
        image = form.save(commit=False)
        product = Product.objects.get(id=self.kwargs['pk'])
        image.product = product
        image.save()
        image_cropper(form.cleaned_data.get('x'),form.cleaned_data.get('y'),
                    form.cleaned_data.get('width'),form.cleaned_data.get('height'),
                    image.product_image,400,400)
        messages.success(self.request,"Image Added Successfully!")
        return redirect("admin:product_detail",pk=product.id)

@method_decorator(decorators,name='dispatch')
class CreatePrice(LoginRequiredMixin,CreateView):
    model = ProductPrice
    form_class = ProductPriceForm

    def form_valid(self,form):
        price = form.save(commit=False)
        product = Product.objects.get(id=self.kwargs['pk'])
        price.product = product
        price.save()
        messages.success(self.request,"New Product Price Added Successfully!")
        return redirect("admin:product_detail",pk=product.id)

@method_decorator(decorators,name='dispatch')
class CreateDose(LoginRequiredMixin,CreateView):
    model = Dose
    form_class = DoseForm

    def form_valid(self,form):
        data = form.save(commit=False)
        data.created_by = self.request.user
        data.save()
        messages.success(self.request,"Product Dose Created Successfully!")
        return redirect("admin:settings")

@method_decorator(decorators,name='dispatch')
class UpdateDose(LoginRequiredMixin,UpdateView):
    model = Dose
    form_class = DoseForm
    template_name = "admin/accounts/check_list_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "product_dose"
        return context

    def form_valid(self,form):
        data = form.save(commit=False)
        data.last_updated_by = self.request.user
        data.last_updated_date = timezone.now()
        data.save()
        messages.success(self.request,"Product Dose Updated Successfully!")
        return redirect("admin:settings")

@method_decorator(decorators,name='dispatch')
class CreateDosageForm(LoginRequiredMixin,CreateView):
    model = DosageForm
    form_class = DosageFormForm

    def form_valid(self,form):
        data = form.save(commit=False)
        data.created_by = self.request.user
        data.save()
        messages.success(self.request,"Product Dosage Form Created Successfully!")
        return redirect("admin:settings")

@method_decorator(decorators,name='dispatch')
class UpdateDosageForm(LoginRequiredMixin,UpdateView):
    model = DosageForm
    form_class = DosageFormForm
    template_name = "admin/accounts/check_list_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "product_dosage"
        return context

    def form_valid(self,form):
        data = form.save(commit=False)
        data.last_updated_by = self.request.user
        data.last_updated_date = timezone.now()
        data.save()
        messages.success(self.request,"Product Dosage Form Updated Successfully!")
        return redirect("admin:settings")

@method_decorator(decorators,name='dispatch')
class ListProductionCapacity(LoginRequiredMixin,ListView):
    model = ProductionCapacity
    template_name = "admin/product/product_data_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProductionCapacity.objects.all()
        else:
            return ProductionCapacity.objects.filter(company=self.request.user.get_company())
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # context['product']=Product.objects.get(id=self.kwargs['product'])
        context['flag'] = "production_capacity"
        return context

@method_decorator(decorators,name='dispatch')
class CreateProductionCapacity(LoginRequiredMixin,CreateView):
    model=ProductionCapacity
    form_class=ProductionCapacityForm
    template_name = "admin/product/product_data_create.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "production_capacity"
        return context
    
    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(CreateProductionCapacity,self).get_form_kwargs()
        
        if self.request.user.is_superuser:
            kwargs.update({'product':SubCategory.objects.all()})
        elif self.request.user.is_company_admin:
            kwargs.update({'company': Company.objects.get(contact_person=self.request.user),
            'product':SubCategory.objects.filter(category_name__in=Company.objects.get(contact_person=self.request.user).category.all())})
        elif self.request.user.is_company_staff:
            kwargs.update({'company': CompanyStaff.objects.get(user=self.request.user).company,
            'product':SubCategory.objects.filter(category_name__in=CompanyStaff.objects.get(user=self.request.user).company.category.all())})
        return kwargs

    def form_valid(self,form):
        if ProductionCapacity.objects.filter(company=self.request.user.get_company(),product=SubCategory.objects.get(id=form.cleaned_data.get('product').id),year=form.cleaned_data.get("year")).exists():
            messages.warning(self.request,"Data For this Year already exists")
            return redirect("admin:create_production_capacity")
        else:
            pc = form.save(commit=False)
            pc.company = self.request.user.get_company()
            pc.created_by = self.request.user
            pc.save()
            messages.success(self.request,"Production Capacity Created")
            return redirect("admin:production_capacity")
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:create_production_capacity")

@method_decorator(decorators,name='dispatch')
class UpdateProductionCapacity(LoginRequiredMixin,UpdateView):
    model=ProductionCapacity
    form_class = ProductionCapacityForm
    template_name = "admin/product/product_data_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "production_capacity"
        return context

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(UpdateProductionCapacity,self).get_form_kwargs()
        if self.request.user.is_superuser:
            kwargs.update({'product':SubCategory.objects.all()})
        elif self.request.user.is_company_admin:
            kwargs.update({'company': Company.objects.get(contact_person=self.request.user),'product':SubCategory.objects.filter(category_name__in=Company.objects.get(contact_person=self.request.user).category.all())})
        elif self.request.user.is_company_staff:
            kwargs.update({'company': CompanyStaff.objects.get(user=self.request.user).company,'product':SubCategory.objects.filter(category_name__in=CompanyStaff.objects.get(user=self.request.user).company.category.all())})
        return kwargs

    def form_valid(self,form):
        pc = form.save(commit=False)
        pc.last_updated_by = self.request.user
        pc.last_updated_date = timezone.now()
        pc.save()
        messages.success(self.request,"Production Capacity Updated")
        return redirect("admin:production_capacity")

    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:update_production_capacity",pk=self.kwargs['pk'])

@method_decorator(decorators,name='dispatch')
class ListSalesPerformance(LoginRequiredMixin,ListView):
    model = ProductionAndSalesPerformance
    template_name = "admin/product/product_data_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProductionAndSalesPerformance.objects.all()
        else:
            return ProductionAndSalesPerformance.objects.filter(company=self.request.user.get_company())
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "sales_performance"
        return context

@method_decorator(decorators,name='dispatch')
class CreateSalesPerformance(LoginRequiredMixin,CreateView):
    model=ProductionAndSalesPerformance
    form_class=SalesPerformanceForm
    template_name = "admin/product/product_data_create.html"

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(CreateSalesPerformance,self).get_form_kwargs()
        if self.request.user.is_superuser:
            kwargs.update({'product':SubCategory.objects.all(),'company':self.request.user.get_company()})
        elif self.request.user.is_company_admin:
            kwargs.update({'product':SubCategory.objects.filter(
                                    category_name__in=Company.objects.get(contact_person=self.request.user).category.all()),
                            'company':self.request.user.get_company()})
        elif self.request.user.is_company_staff:
            kwargs.update({'product':SubCategory.objects.filter(
                                    category_name__in=CompanyStaff.objects.get(user=self.request.user).company.category.all()),
                                'company':self.request.user.get_company()})
        return kwargs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "sales_performance"
        return context

    def form_valid(self,form):
        if ProductionAndSalesPerformance.objects.filter(company=self.request.user.get_company(),
            product=SubCategory.objects.get(id=form.cleaned_data.get('product').id)
            ,activity_year=form.cleaned_data.get('activity_year'),half_year=form.cleaned_data.get('half_year')).exists():
            messages.warning(self.request,"Data For this Year already exists")
            return redirect("admin:create_sales_performance")
        else:
            sp = form.save(commit=False)
            sp.company = self.request.user.get_company()
            sp.created_by = self.request.user
            sp.save()
            messages.success(self.request,"Production Sales Performance Created")
            # return redirect("admin:create_sales_performance")
            return redirect("admin:sales_performance")
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:create_sales_performance")

@method_decorator(decorators,name='dispatch')
class UpdateSalesPerformance(LoginRequiredMixin,UpdateView):
    model=ProductionAndSalesPerformance
    form_class = SalesPerformanceForm
    template_name = "admin/product/product_data_update.html"

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(UpdateSalesPerformance,self).get_form_kwargs()
        if self.request.user.is_superuser:
            kwargs.update({'product':SubCategory.objects.all(),'company':self.request.user.get_company()})
        elif self.request.user.is_company_admin:
            kwargs.update({'product':SubCategory.objects.filter(
                                    category_name__in=Company.objects.get(contact_person=self.request.user).category.all()),
                            'company':self.request.user.get_company()})
        elif self.request.user.is_company_staff:
            kwargs.update({'product':SubCategory.objects.filter(
                                    category_name__in=CompanyStaff.objects.get(user=self.request.user).company.category.all()),
                                'company':self.request.user.get_company()})
        return kwargs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "sales_performance"
        return context

    def form_valid(self,form):
        sp = form.save(commit=False)
        sp.last_updated_by = self.request.user
        sp.last_updated_date = timezone.now()
        sp.save()
        messages.success(self.request,"Sales Performance Updated")
        return redirect("admin:sales_performance")
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:update_sales_performance",pk=self.kwargs['pk'])

@method_decorator(decorators,name='dispatch')
class ListPackaging(LoginRequiredMixin,ListView):
    model = ProductPackaging
    template_name = "admin/product/product_data_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProductPackaging.objects.all()
        else:
            return ProductPackaging.objects.filter(company=self.request.user.get_company())
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "packaging"
        return context

@method_decorator(decorators,name='dispatch')
class CreatePackaging(LoginRequiredMixin,CreateView):
    model=ProductPackaging
    form_class=ProductPackagingForm
    template_name = "admin/product/product_data_create.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "packaging"
        return context

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(CreatePackaging,self).get_form_kwargs()
        if self.request.user.is_superuser:
            kwargs.update({'product':SubCategory.objects.all()})
        elif self.request.user.is_company_admin:
            kwargs.update({'product':SubCategory.objects.filter(category_name__in=Company.objects.get(contact_person=self.request.user).category.all())})
        elif self.request.user.is_company_staff:
            kwargs.update({'product':SubCategory.objects.filter(category_name__in=CompanyStaff.objects.get(user=self.request.user).company.category.all())})
        return kwargs

    def form_valid(self,form):
        sp = form.save(commit=False)
        sp.company = self.request.user.get_company()
        sp.created_by = self.request.user
        sp.save()
        messages.success(self.request,"Product Packaging Created")
        # return redirect('admin:create_packaging')
        return redirect("admin:packaging")
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect('admin:create_packaging')


@method_decorator(decorators,name='dispatch')
class UpdatePackaging(LoginRequiredMixin,UpdateView):
    model=ProductPackaging
    form_class = ProductPackagingForm
    template_name = "admin/product/product_data_update.html"

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(UpdatePackaging,self).get_form_kwargs()
        if self.request.user.is_superuser:
            kwargs.update({'product':SubCategory.objects.all()})
        elif self.request.user.is_company_admin:
            kwargs.update({'product':SubCategory.objects.filter(category_name__in=Company.objects.get(contact_person=self.request.user).category.all())})
        elif self.request.user.is_company_staff:
            kwargs.update({'product':SubCategory.objects.filter(category_name__in=CompanyStaff.objects.get(user=self.request.user).company.category.all())})
        return kwargs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "packaging"
        return context

    def form_valid(self,form):
        sp = form.save(commit=False)
        sp.last_updated_by = self.request.user
        sp.last_updated_date = timezone.now()
        sp.save()
        messages.success(self.request,"Packaging Data Updated")
        return redirect("admin:packaging")
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:update_packaging",pk=self.kwargs['pk'])

@method_decorator(decorators,name='dispatch')
class ListAnualInputNeed(LoginRequiredMixin,ListView):
    model = AnnualInputNeed
    template_name = "admin/product/product_data_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return AnnualInputNeed.objects.all()
        else:
            return AnnualInputNeed.objects.filter(company=self.request.user.get_company())
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "anual_input_need"
        return context

@method_decorator(decorators,name='dispatch')
class CreateAnualInputNeed(LoginRequiredMixin,CreateView):
    model=AnnualInputNeed
    form_class=AnualInputNeedForm
    template_name = "admin/product/product_data_create.html"

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(CreateAnualInputNeed,self).get_form_kwargs()
        if self.request.user.is_superuser:
            kwargs.update({'product':SubCategory.objects.all(),'company':self.request.user.get_company()})
        elif self.request.user.is_company_admin:
            kwargs.update({'product':SubCategory.objects.filter(
                                    category_name__in=Company.objects.get(contact_person=self.request.user).category.all()),
                            'company':self.request.user.get_company()})
        elif self.request.user.is_company_staff:
            kwargs.update({'product':SubCategory.objects.filter(
                                    category_name__in=CompanyStaff.objects.get(user=self.request.user).company.category.all()),
                                'company':self.request.user.get_company()})
        return kwargs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "anual_input_need"
        return context

    def form_valid(self,form):
        if AnnualInputNeed.objects.filter(company=self.request.user.get_company(),product=SubCategory.objects.get(id=form.cleaned_data.get('product').id),year=form.cleaned_data.get('year'),
            input_name =form.cleaned_data.get("input_name")).exists():
            messages.warning(self.request,"Data For this Input and Year already exists")
            return redirect("admin:create_anual_inp_need")
        else:
            ain = form.save(commit=False)
            ain.company = self.request.user.get_company()
            ain.created_by = self.request.user
            ain.save()
            messages.success(self.request,"Anual Input Need Created")
            # return redirect("admin:create_anual_inp_need")
            return redirect("admin:anual_input_need")

@method_decorator(decorators,name='dispatch')
class UpdateAnualInputNeed(LoginRequiredMixin,UpdateView):
    model=AnnualInputNeed
    form_class = AnualInputNeedForm
    template_name = "admin/product/product_data_update.html"

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(UpdateAnualInputNeed,self).get_form_kwargs()
        if self.request.user.is_superuser:
            kwargs.update({'product':SubCategory.objects.all(),'company':self.request.user.get_company()})
        elif self.request.user.is_company_admin:
            kwargs.update({'product':SubCategory.objects.filter(
                                    category_name__in=Company.objects.get(contact_person=self.request.user).category.all()),
                            'company':self.request.user.get_company()})
        elif self.request.user.is_company_staff:
            kwargs.update({'product':SubCategory.objects.filter(
                                    category_name__in=CompanyStaff.objects.get(user=self.request.user).company.category.all()),
                                    'company':self.request.user.get_company()})
        return kwargs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "anual_input_need"
        return context

    def form_valid(self,form):
        ain = form.save(commit=False)
        ain.last_updated_by = self.request.user
        ain.last_updated_date = timezone.now()
        ain.save()
        messages.success(self.request,"Product Anual Input Need Updated")
        return redirect("admin:anual_input_need")
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:update_anual_inp_need",pk=self.kwargs['id'])


@method_decorator(decorators,name='dispatch')
class ListInputDemandSupply(LoginRequiredMixin,ListView):
    model = InputDemandSupply
    template_name = "admin/product/product_data_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return InputDemandSupply.objects.all()
        else:
            return InputDemandSupply.objects.filter(company=self.request.user.get_company())
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "demand_supply"
        return context

@method_decorator(decorators,name='dispatch')
class CreateInputDemandSupply(LoginRequiredMixin,CreateView):
    model=InputDemandSupply
    form_class=InputDemandSupplyForm
    template_name = "admin/product/product_data_create.html"

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(CreateInputDemandSupply,self).get_form_kwargs()
        if self.request.user.is_superuser:
            kwargs.update({'product':SubCategory.objects.all(),'company':self.request.user.get_company()})
        elif self.request.user.is_company_admin:
            kwargs.update({'product':SubCategory.objects.filter(
                                    category_name__in=Company.objects.get(contact_person=self.request.user).category.all()),
                            'company':self.request.user.get_company()})
        elif self.request.user.is_company_staff:
            kwargs.update({'product':SubCategory.objects.filter(
                                    category_name__in=CompanyStaff.objects.get(user=self.request.user).company.category.all()),
                                    'company':self.request.user.get_company()})
        return kwargs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "demand_supply"
        return context

    def form_valid(self,form):
        if InputDemandSupply.objects.filter(company=self.request.user.get_company(),
                            product=form.cleaned_data.get('product').id,
                            year=form.cleaned_data.get('year'),half_year=form.cleaned_data.get("half_year"),input_type=form.cleaned_data.get('input_type')).exists():
            messages.warning(self.request,"Data For this Year already exists")
            return redirect("admin:create_demand_supply")
        else:
            ds = form.save(commit=False)
            ds.company=self.request.user.get_company()
            ds.created_by = self.request.user
            ds.save()
            messages.success(self.request,"Input Demand and Supply data added")
            # return redirect("admin:create_demand_supply")
            return redirect("admin:demand_supply_list")
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:create_demand_supply")

@method_decorator(decorators,name='dispatch')
class UpdateInputDemandSupply(LoginRequiredMixin,UpdateView):
    model=InputDemandSupply
    form_class = InputDemandSupplyForm
    template_name = "admin/product/product_data_update.html"

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(UpdateInputDemandSupply,self).get_form_kwargs()
        if self.request.user.is_superuser:
            kwargs.update({'product':SubCategory.objects.all(),'company':self.request.user.get_company()})
        elif self.request.user.is_company_admin:
            kwargs.update({'product':SubCategory.objects.filter(
                                    category_name__in=Company.objects.get(contact_person=self.request.user).category.all()),
                            'company':self.request.user.get_company()})
        elif self.request.user.is_company_staff:
            kwargs.update({'product':SubCategory.objects.filter(
                                    category_name__in=CompanyStaff.objects.get(user=self.request.user).company.category.all()),
                                    'company':self.request.user.get_company()})
        return kwargs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "demand_supply"
        return context

    def form_valid(self,form):
        ds = form.save(commit=False)
        ds.last_updated_by = self.request.user
        ds.last_updated_date = timezone.now()
        ds.save()
        messages.success(self.request,"Product Input Demand and supply data Updated")
        return redirect("admin:demand_supply_list")
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:update_demand_supply",pk=self.kwargs['pk'])



 

 
class p_serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id","name", "name_am",  "image")

@login_required
def FetchInquiryProducts(request):
    data = json.loads(request.body)
    # remove the last , from the incoming string
    prods_id_list = data['products'][:-1] 
    product_ids = prods_id_list.split(",")
    product_list = [int(i) for i in product_ids]
    products = Product.objects.filter(id__in = product_list).distinct()
    return JsonResponse( p_serializer(products, many = True).data, safe = False)

# this function is used, because to convert the list of string ids to integer and to cut the last , off
def get_id_list(str_id):
    prods_id_list = str_id[:-1] 
    product_ids = prods_id_list.split(",")
    return [int(i) for i in product_ids]

    

class InquiryRequest(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            selected_prods = Product.objects.filter(id__in = get_id_list( self.request.GET['products']) )
            context = {'products':selected_prods,'prod_id_list': self.request.GET['products'],'form':ProductInquiryForm}
            if selected_prods.count() > 1:
                context['product_count'] = selected_prods.count()
            return render(self.request, "frontpages/product/inquiry_form.html", context)
        except Exception as e:
            print("@@@@@@ Exception at InquiryForm get ",e)
            return redirect ('index')

    def post(self, *args,**kwargs):
        try:
            products = Product.objects.filter(id__in = get_id_list( self.request.POST['prod_id_list']) ).distinct()
            form = ProductInquiryForm(self.request.POST)
            if form.is_valid:
                for p in products:       
                    item = form.save(commit = False)
                    item.product = p
                    item.user=self.request.user
                    item.save()
            else:
                print("form invalid")
            return render(self.request, "frontpages/product/success_inquiry.html",{ 'email':self.request.POST['sender_email'], 'prod_id_list': self.request.POST['prod_id_list'] })
        except Exception as e:
            print("@@@ Exception ",e)
            return redirect("index")
    
class InquiryByCategory(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            category = self.request.GET.getlist('category')[0]            
            companies = Company.objects.filter(category = category )
            company_ids = [c.id for c in companies ]
            context = {'company_ids':company_ids,'count':len(company_ids),'category':category,'form':ProductInquiryForm}
            return render(self.request, "frontpages/product/category_inquiry_form.html", context)
    
        except Exception as e:
            print("@@@@@@ Exception at InquiryByCategory get ",e)
            return redirect ('index')
    
    def post(self, *args,**kwargs):
        try:
            category = Category.objects.get(id = int(self.request.POST['category']))
            companies = category.company_category.all()
            form = ProductInquiryForm(self.request.POST)
            if form.is_valid:
                for c in companies:       
                    item = form.save(commit = False)
                    item.category = category
                    item.user=self.request.user
                    item.save()
                    return render(self.request, "frontpages/product/success_inquiry.html",{ 'email':self.request.POST['sender_email'], 'prod_id_list': [] })        
            else:
                print("invalid data")
                return redirect("index")

        except Exception as e:
            print("@@@ Exception ",e)
            return redirect("index")

@login_required
def LikeProduct(request):
    try:
        data = json.loads( request.body )
        p_like = ProductLike(user = request.user, product = Product.objects.get (id= int(data['p_id'] ) )  )
        p_like.save()
        return JsonResponse({'error':False})

    except Exception as e:
        print("########Exception while tring to like a product ",e)
        return JsonResponse({'error':True})



################### newly added , delete this comment
class ProductByCategoryView(ListView):
    model=Product
    template_name="frontpages/product/product_category.html"
    paginate_by = 3
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(category_type=Category.objects.get(id=self.kwargs['cat_id']).category_type)
      
        return context

    def get_queryset(self):
        category = Category.objects.get(id=self.kwargs['cat_id'])
        brands = []
        for sub_cat in category.sub_category.all():
            for brand in sub_cat.product_category.all():
                brands.append(brand)
        return Product.objects.filter(brand__in=brands)
        # if category.category_type == "Pharmaceuticals":
        #     return Product.objects.filter(
        #         pharmacy_category=category)
        # elif category.category_type == "Food" or category.category_type == "Beverage":
            
class ProductByProductView(ListView):
    model=Product
    template_name="frontpages/product/product_category.html"
    paginate_by = 3
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = SubCategory.objects.filter(category_name=SubCategory.objects.get(id=self.kwargs['cat_id']).category_name)
      
        return context

    def get_queryset(self):
        category = SubCategory.objects.get(id=self.kwargs['cat_id'])
        brands = []
        for brand in category.product_category.all():
            brands.append(brand)
        return Product.objects.filter(brand__in=brands)



class ProductByMainCategory(ListView):
    model=Product
    template_name="frontpages/product/product_category.html"
    paginate_by = 6

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(category_type=self.kwargs['option'])
        return context

    def get_queryset(self):
        brands = []
        if self.kwargs['option'] == "Beverage":
            categories = Category.objects.filter(category_type="Beverage")
            for category in categories:
                for sub_cat in category.sub_category.all():
                    for brand in sub_cat.product_category.all():
                        brands.append(brand)
            return Product.objects.filter(brand__in = brands)
        elif self.kwargs['option'] == "Food":
            categories = Category.objects.filter(category_type="Food")
            for category in categories:
                for sub_cat in category.sub_category.all():
                    for brand in sub_cat.product_category.all():
                        brands.append(brand)
            return Product.objects.filter(brand__in=brands)
        elif self.kwargs['option'] == "Pharmaceuticals":
            categories = Category.objects.filter(category_type="Pharmaceuticals")
            for category in categories:
                for sub_cat in category.sub_category.all():
                    for brand in sub_cat.product_category.all():
                        brands.append(brand)
            return Product.objects.filter(brand__in=brands)
            # return Product.objects.filter(pharmacy_category__in=Category.objects.filter(category_type="Pharmaceuticals"))
        elif self.kwargs['option'] == "all":
            return Product.objects.all()

class SearchProduct(View):

    def get(self,*args,**kwargs):
        template_name = "frontpages/product/product_category.html"
        products = Product.objects.all()
        if 'name' in self.request.GET and self.request.GET['name'] != '':
            products = Product.objects.filter(
                Q(name__icontains=self.request.GET['name'])|Q(name_am__icontains=self.request.GET['name'])|Q(brand__brand_name__icontains=self.request.GET['name'])|Q(brand__product_type__sub_category_name__icontains=self.request.GET['name'])
                ).distinct()
        try:
            if 'sector' in self.request.GET:
                if self.request.GET['sector'] !='' or self.request.GET['sector'] != "Select":
                    products = products.filter(Q(brand__product_type__category_name__id=self.request.GET['sector'])).distinct()
        except ValueError as e:
            products = products 
        return render(self.request,template_name,{'object_list':products, })
        
class ProductDetailView(DetailView):
    model = Product
    template_name = "frontpages/product/product_detail.html"

    def get_object(self):
        try:
            return Product.objects.get(id=self.kwargs['pk'])
        except Product.DoesNotExist:
            return None
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(brand=Product.objects.get(id=self.kwargs['pk']).brand)[:6]
        context['reviews'] = Review.objects.filter(product=Product.objects.get(id=self.kwargs['pk']))
        context['form'] = ReviewForm
        return context


class CreateReview(CreateView):
    model=Review
    form_class = ReviewForm

    def form_valid(self, form):
        review = form.save(commit=False)
        review.product = Product.objects.get(id=self.kwargs['product'])
        review.save()
        return redirect('product_detail',pk=self.kwargs['product'])
    
    def form_invalid(self,form):
        print("invalid form ",form.errors)
        return redirect('product_detail',pk=self.kwargs['product'])


class CategoriesView(ListView):
    template_name = "frontpages/product/categories.html"

    def get_queryset(self):
        return SubCategory.objects.filter(category_name__category_type=self.kwargs['category'])