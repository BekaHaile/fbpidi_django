import random
import string

from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View,ListView,UpdateView,CreateView,DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from django.db.models import Q

from admin_site.models import Category
from product.models import *
from product.forms import *
from company.models import *



def create_ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits,k=30))

def create_invoice(invoice,user):
    return '#INV-'.join(random.choices(string.ascii_uppercase + (invoice.join(user.id))))

# This is class/view is crated for displaying all categories and sub categories 
class CategoryView(LoginRequiredMixin,ListView):
    model = Category
    template_name = "admin/product/categories.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = True
        return context

# This class/view is created for displaying category and sub category detail and editing
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
        messages.success(self.request,"You Created a New Category")
        return redirect("admin:categories")
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = True
        return context

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
        messages.success(self.request,"You Updated a Product Type")
        return redirect("admin:sub_categories")
    
    def form_invalid(self,form):
        message.warning(self.request,form.errors)
        return redirect("admin:edit_subcategory",pk=self.kwargs['pk']) 

# This class/view is created for creating new categories
class CreateSubCategories(LoginRequiredMixin,CreateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = "admin/product/category_form_create.html"
    

    def form_valid(self,form):        
        sub_category = form.save(commit=False)
        sub_category.created_by = self.request.user
        sub_category.save()
        messages.success(self.request,"You Created a New Product Type")
        return redirect("admin:sub_categories")
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_category'] = True
        return context
    
    def form_invalid(self,form):
        message.warning(self.request,form.errors)
        return redirect("admin:create_subcategory",pk=self.kwargs['pk']) 




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
        messages.success(self.request,"Product Created Successfully!")
        return redirect("admin:admin_products")
    


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
        messages.success(self.request,"Product Update Successfully!")
        return redirect("admin:admin_products")

class AddProductImage(LoginRequiredMixin,CreateView):
    model=ProductImage
    form_class = ProductImageForm

    def form_valid(self,form):
        image = form.save(commit=False)
        product = Product.objects.get(id=self.kwargs['pk'])
        image.product = product
        image.save()
        messages.success(self.request,"Image Added Successfully!")
        return redirect("admin:product_detail",pk=product.id)


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


class CreateDose(LoginRequiredMixin,CreateView):
    model = Dose
    form_class = DoseForm

    def form_valid(self,form):
        data = form.save(commit=False)
        data.created_by = self.request.user
        data.save()
        messages.success(self.request,"Product Dose Created Successfully!")
        return redirect("admin:settings")

 
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

class CreateDosageForm(LoginRequiredMixin,CreateView):
    model = DosageForm
    form_class = DosageFormForm

    def form_valid(self,form):
        data = form.save(commit=False)
        data.created_by = self.request.user
        data.save()
        messages.success(self.request,"Product Dosage Form Created Successfully!")
        return redirect("admin:settings")


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
            kwargs.update({'product':SubCategory.objects.filter(category_name__in=Company.objects.get(contact_person=self.request.user).category.all())})
        elif self.request.user.is_company_staff:
            kwargs.update({'product':SubCategory.objects.filter(category_name__in=CompanyStaff.objects.get(user=self.request.user).company.category.all())})
        return kwargs

    def form_valid(self,form):
        if ProductionCapacity.objects.filter(company=self.request.user.get_company(),product=SubCategory.objects.get(id=form.cleaned_data.get('product').id),p_date=form.cleaned_data.get('p_date')).exists():
            messages.warning(self.request,"Data For this Day already exists")
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
            kwargs.update({'product':SubCategory.objects.filter(category_name__in=Company.objects.get(contact_person=self.request.user).category.all())})
        elif self.request.user.is_company_staff:
            kwargs.update({'product':SubCategory.objects.filter(category_name__in=CompanyStaff.objects.get(user=self.request.user).company.category.all())})
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
            ,activity_year=form.cleaned_data.get('activity_year')).exists():
            messages.warning(self.request,"Data For this Year already exists")
            return redirect("admin:create_sales_performance")
        else:
            sp = form.save(commit=False)
            sp.company = self.request.user.get_company()
            sp.created_by = self.request.user
            sp.save()
            messages.success(self.request,"Production Sales Performance Created")
            return redirect("admin:sales_performance")
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:create_sales_performance")


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
        return redirect("admin:packaging")
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect('admin:create_packaging')


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
            input_name__icontains =form.cleaned_data.get("input_name")).exists():
            messages.warning(self.request,"Data For this Input and Year already exists")
            return redirect("admin:create_anual_inp_need")
        else:
            ain = form.save(commit=False)
            ain.company = self.request.user.get_company()
            ain.created_by = self.request.user
            ain.save()
            messages.success(self.request,"Anual Input Need Created")
            return redirect("admin:anual_input_need")


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
                            year=form.cleaned_data.get('year'),input_type=form.cleaned_data.get('input_type')).exists():
            messages.warning(self.request,"Data For this Year already exists")
            return redirect("admin:create_demand_supply")
        else:
            ds = form.save(commit=False)
            ds.company=self.request.user.get_company()
            ds.created_by = self.request.user
            ds.save()
            messages.success(self.request,"Input Demand and Supply data added")
            return redirect("admin:demand_supply_list")
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:create_demand_supply")


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




# 
class AddToCartView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        product = get_object_or_404(Product,id=kwargs['id'])
        
        order_product,created = OrderProduct.objects.get_or_create(
            product=product,
            to_company=product.company,
            user=self.request.user,
            ordered=False
        )
        order_queryset = Order.objects.filter(
            user=self.request.user,
            ordered=False
        )
        if order_queryset.exists():
            order = order_queryset[0]
            if order.products.filter(product__id=product.id).exists():
                order_product.quantity +=1
                order_product.save()
                return redirect("cart_summary")
            else:
                order.products.add(order_product)
                order.save()
                messages.success(self.request,"New Product is added to your cart")
                return redirect("cart_summary")
        else:
            order = Order.objects.create(user=self.request.user,order_date=timezone.now())
            order.products.add(order_product)
            order.save()
            messages.success(self.request,"The Order is added to your cart")
            return redirect("cart_summary")


class CartSummary(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            products = Product.objects.all().order_by("timestamp")[:4]
            return  render(self.request,"frontpages/product/carts.html",{'orders':order,'products':products})
        except ObjectDoesNotExist:
            messages.warning(self.request,"You Do Not have active order")
            return redirect("index")


class DecrementFromCart(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        product = get_object_or_404(Product,id=self.kwargs['id'])
        order_qset = Order.objects.filter(user=self.request.user,ordered=False)
        if order_qset.exists():
            order = order_qset[0]
            if order.products.filter(product__id=product.id).exists():
                print("here")
                order_product = OrderProduct.objects.filter( 
                    user=self.request.user,product=product,ordered=False )[0]
                if order_product.quantity > 1:
                    order_product.quantity -= 1
                    order_product.save()
                    return redirect("cart_summary")
                else:
                    order.products.remove(order_product)
                    messages.success(self.request,"All Items removed from your cart")
                    return redirect("index")
                
               
            else: 
                messages.warning(self.request,"This item was not in your cart")
                return redirect("index")
        else: 
            messages.warning(self.request,"You do not have order")
            return redirect("index")    

class CheckoutView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = {}
        order = Order.objects.get(user=self.request.user,ordered=False)
        context['order'] = order
        context['form'] = CheckoutForm()
        return render(self.request,"frontpages/product/checkout.html",context)

    
    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST)
        order = Order.objects.get(user=self.request.user,ordered=False)
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.user = self.request.user
            shipping.save()
            order.shipping_address = shipping
            invoice = InvoiceRecord.create(
                user=self.request.user,
                amount=order.get_total_price()
            )
            invoice.code = create_invoice(invoice,self.request.user)
            invoice.save()
            order.invoice = invoice
            order.ordered = True
            order.save()
            return redirect("")

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
            



class ProductByMainCategory(ListView):
    model=Product
    template_name="frontpages/product/product_category.html"
    paginate_by = 3

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
            return Product.objects.filter(brand__in=brands)
        elif self.kwargs['option'] == "Food":
            categories = Category.objects.filter(category_type="Food")
            for category in categories:
                for sub_cat in category.sub_category.all():
                    for brand in sub_cat.product_category.all():
                        brands.append(brand)
            return Product.objects.filter(brand__in=brands)
        elif self.kwargs['option'] == "Pharmaceuticals":
            categories = Category.objects.filter(category_type="Food")
            for category in categories:
                for sub_cat in category.sub_category.all():
                    for brand in sub_cat.product_category.all():
                        brands.append(brand)
            return Product.objects.filter(brand__in=brands)
            # return Product.objects.filter(pharmacy_category__in=Category.objects.filter(category_type="Pharmaceuticals"))
        elif self.kwargs['option'] == "all":
            return Product.objects.all()

class ProductDetailView(DetailView):
    model = Product
    template_name = "frontpages/product/product_detail.html"

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
        
