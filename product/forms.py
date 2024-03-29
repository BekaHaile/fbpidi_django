import datetime

from django import forms
from django.db.transaction import atomic
from django.forms import widgets

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from PIL import Image

from product.models import *
from admin_site.models import Category
from company.models import Company, CompanyStaff,InvestmentProject


def return_year(start_year):
    current_year = 0
    gc_year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    day = datetime.datetime.today().day
    print(month)
    if month <= 7 and day < 8 or month <= 7:
        current_year = gc_year-9
    else:
        current_year = gc_year - 8
    YEAR_CHOICES=[('','Select Year'),]
    YEAR_CHOICES += [(r,r) for r in range(start_year, current_year+1)]
    return YEAR_CHOICES

def in_between(x,min,max):
    return ((x-min)*(x-max) <= 0)

def return_year_with_halfyear(start_year):
    current_year = 0
    gc_year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    day = datetime.datetime.today().day
    if in_between(month,1,6):
        current_year = gc_year-8
    else:
        current_year = gc_year - 9
    YEAR_CHOICES=[('','Select Year'),]
    YEAR_CHOICES += [(r,r) for r in range(start_year, current_year+1)]
    return YEAR_CHOICES

class CompanySelectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CompanySelectForm,self).__init__(*args,**kwargs)
        self.fields['company'].queryset = Company.objects.all().order_by('name')
        self.fields['company'].empty_label = "Select company "
    

    class Meta:
        model = Product
        fields = ('company',)
        widgets ={
            'company':forms.Select(attrs={'class':'form-control form-control-uniform'}),

        }
    

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_type','category_name','category_name_am','icons')
        widgets = {
            'icons':forms.FileInput(attrs={'class':"form-control form-input-styled"}),
            'category_type':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'category_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Sub Sector Name(English)'}),
            # 'description':forms.Textarea(attrs={'class':'summernote'}),
            'category_name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Sub Sector Name(Amharic)'}),
            # 'description_am':forms.Textarea(attrs={'class':'summernote'}),
        }


class BrandForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.company = kwargs.pop('company')
        super(BrandForm,self).__init__(*args,**kwargs)
        self.fields['product_type'].empty_label = "Select A Product Type"
        self.fields['product_type'].queryset = SubCategory.objects.filter(category_name__in=self.company.category.all())
        
    class Meta:
        model = Brand
        fields = ('product_type','brand_name','brand_name_am',)
        widgets = {
            'product_type':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'brand_name':forms.TextInput(attrs={'placeholder':'Product Brand Name'}),
            'brand_name_am':forms.TextInput(attrs={'placeholder':'Product Brand Name in Amharic'})
        }


class SubCategoryForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(SubCategoryForm,self).__init__(*args,**kwargs)
        self.fields['category_name'].queryset = Category.objects.all()
        self.fields['category_name'].empty_label = "Select Sub Sector"
        self.fields['uom'].empty_label = "Select Unit of Measurement"

   

    class Meta:
        model = SubCategory
        fields = ('category_name','sub_category_name','description','sub_category_name_am','description_am','uom','icons')
        widgets = {
            'icons':forms.FileInput(attrs={'class':"form-control form-input-styled"}),
            'category_name':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'sub_category_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Product Name(English)'}),
            'uom':forms.Select(attrs={'class':'form-control form-control-uniform','placeholder':'Unit Of Measurement'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'sub_category_name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Product Name(Amharic)'}),
            'description_am':forms.Textarea(attrs={'class':'summernote'}),
        } 


class ProductCreationForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y = forms.FloatField(widget=forms.HiddenInput(),required=False)
    width = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height = forms.FloatField(widget=forms.HiddenInput(),required=False)

    def __init__(self,*args,**kwargs):
        self.company = kwargs.pop('company')
        super(ProductCreationForm,self).__init__(*args,**kwargs)
        self.fields['project'].empty_label = "Select The Project"
        self.fields['project'].queryset = InvestmentProject.objects.filter(company=self.company,project_complete=True)
        self.fields['brand'].queryset = Brand.objects.filter(company=self.company)
        # if self.company.main_category == 'FBPIDI':
        #      self.fields['pharmacy_category'].queryset = Category.objects.filter(category_type="Pharmaceuticals")
        # else:
        #     self.fields['pharmacy_category'].queryset = Category.objects.filter(category_type=self.company.main_category)
        # self.fields['dose'].queryset = Dose.objects.all()
        if self.company.main_category == "Pharmaceuticals":
            self.fields['brand'].required = False
            company_categories = self.company.category.all()
            self.fields['pharmacy_product_type'].queryset = SubCategory.objects.filter(category_name__in = company_categories)
            self.fields['pharmacy_product_type'].required = True

            
        else:
            self.fields['brand'].required = False
            self.fields['pharmacy_product_type'].required = False
        
        self.fields['dosage_form'].queryset = DosageForm.objects.all()
        # self.fields['dose'].empty_label = "Select Prodect Dose"
        self.fields['pharmacy_product_type'].empty_label = "Select Product Type"
        self.fields['dosage_form'].empty_label = "Select Product Dosage Form"
        self.fields['brand'].empty_label = "Select Product Brand"
        self.fields['reserve_attr0'].empty_label = "Select Product Group"
        self.fields['therapeutic_group'].empty_label = "Select Therapeutic Group"
     
    class Meta:
        model = Product
        fields = ('name','name_am','project','brand','reserve_attr0',
                    'dose','dosage_form','quantity','therapeutic_group','pharmacy_product_type',
                    'description','description_am','image',)
        widgets = {
            'project':forms.Select(attrs={'class':'form-control form-control-uniform','required':False}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Product/Varayti Name(English)'}),
            'name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Product/Varayti Name(Amharic)'}),
            'brand':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'pharmacy_product_type':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'reserve_attr0':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'dose':forms.TextInput(attrs={'class':'form-control','placeholder':'Dose & Packaging'}),
            'dosage_form':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'therapeutic_group':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'description':forms.Textarea(attrs={'class':'summernote','required':'False'}),
            'description_am':forms.Textarea(attrs={'class':'summernote','required':'False'}),
            'image':forms.FileInput(attrs={'class':"form-control form-input-styled"}),
            'quantity':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_quantity")'}),
        } 


class PharmaceuticalProductCreationForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y = forms.FloatField(widget=forms.HiddenInput(),required=False)
    width = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height = forms.FloatField(widget=forms.HiddenInput(),required=False)

    def __init__(self,*args,**kwargs):
        self.company = kwargs.pop('company')
        # self.user = kwargs.pop('user')
        super(PharmaceuticalProductCreationForm,self).__init__(*args,**kwargs)
        self.fields['brand'].queryset = Brand.objects.filter(company=self.company)
        self.fields['brand'].required = False
        self.fields['dose'].queryset = Dose.objects.all()
        self.fields['dosage_form'].queryset = DosageForm.objects.all()
        self.fields['project'].empty_label = "Select The Project"
        self.fields['project'].queryset = InvestmentProject.objects.filter(company=self.company,project_complete=True)
        company_categories = self.company.category.all()
        self.fields['pharmacy_product_type'].queryset = SubCategory.objects.filter(category_name__in = company_categories)
        self.fields['pharmacy_product_type'].required = True

        # self.fields['dose'].empty_label = "Select Prodect Dose"

        self.fields['dosage_form'].empty_label = "Select Product Dosage Form"
        self.fields['brand'].empty_label = "Select Product Brand"
        self.fields['reserve_attr0'].empty_label = "Select Product Group"
        self.fields['therapeutic_group'].empty_label = "Select Therapeutic Group"
     
    class Meta:
        model = Product
        fields = ('name','name_am','project','brand','reserve_attr0',
                    'dose','dosage_form','quantity','therapeutic_group',
                    'description','description_am','image',)
        widgets = {
            'project':forms.Select(attrs={'class':'form-control form-control-uniform','required':False}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Product/Varayti Name(English)'}),
            'name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Product/Varayti Name(Amharic)'}),
            'brand':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'reserve_attr0':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'dose':forms.TextInput(attrs={'class':'form-control','placeholder':'Dose & Packaging'}),
            'dosage_form':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'therapeutic_group':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'description':forms.Textarea(attrs={'class':'summernote','required':'False'}),
            'description_am':forms.Textarea(attrs={'class':'summernote','required':'False'}),
            'image':forms.FileInput(attrs={'class':"form-control form-input-styled"}),
            'quantity':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_quantity")'}),
        } 
 

class DosageFormForm(forms.ModelForm):
    class Meta:
        model = DosageForm
        fields = ('dosage_form','dosage_form_am',)
        widgets = {
            'dosage_form':forms.TextInput(attrs={'class':'form-control','placeholder':'Dosage Form in English'}),
            'dosage_form_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Dosage Form in Amharic'}),
        }


class DoseForm(forms.ModelForm):
    class Meta:
        model = Dose
        fields = ('dose','dose_am',)
        widgets = {
            'dose':forms.TextInput(attrs={'class':'form-control','placeholder':'Dose in English'}),
            'dose_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Dose in Amharic'}),
            
        }

class ProductionCapacityForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        self.product = kwargs.pop("product")
        self.company = kwargs.pop("company")
        super(ProductionCapacityForm,self).__init__(*args,**kwargs)
        self.fields['product'].queryset = self.product
        self.fields['product'].empty_label = "Select A Product"
        self.fields['year'].empty_label = "Select Year"
        self.fields['year'].widget = forms.Select(choices=
            return_year(self.company.established_yr),
            attrs={'class':'form-control form-control-uniform'}
            )

    class Meta:
        model=ProductionCapacity
        fields = ('product','year','install_prdn_capacity','atnbl_prdn_capacity',
                    'actual_prdn_capacity','production_plan','extraction_rate')
        widgets = {
            'product':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            # 'p_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'install_prdn_capacity':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_install_prdn_capacity")'}),
            'atnbl_prdn_capacity':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_atnbl_prdn_capacity")'}),
            'actual_prdn_capacity':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_actual_prdn_capacity")'}),
            'production_plan':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_production_plan")'}),
            'extraction_rate':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_extraction_rate")'}),
        }

class ProductPackagingForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        self.product = kwargs.pop('product')
        super(ProductPackagingForm,self).__init__(*args,**kwargs)
        self.fields['product'].queryset = self.product
        self.fields['product'].empty_label = "Select Product"
        self.fields['input_unit'].empty_label = "Select Unit of Measurement"

    class Meta:
        model=ProductPackaging
        fields = ('product','packaging','input_unit','category','amount','local_input','import_input','wastage')
        widgets = {
            'packaging':forms.TextInput(attrs={'class':'form-control','placeholder':'Packaging Type'}),
            'product':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'category':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'amount':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_amount")'}),
            'local_input':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_local_input")'}),
            'import_input':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_import_input")'}),
            'wastage':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_wastage")'}),
        }


class SalesPerformanceForm(forms.ModelForm):
    # activity_year = forms.IntegerField(label="Activity Year",widget=forms.Select(choices=YEAR_CHOICES,
    #             attrs={'class':'form-control form-control-uniform'}))

    def __init__(self,*args,**kwargs):
        self.product = kwargs.pop('product')
        self.company = kwargs.pop('company')
        super(SalesPerformanceForm,self).__init__(*args,**kwargs)
        self.fields['activity_year'].empty_label = "Select Year"
        self.fields['activity_year'].widget = forms.Select(choices=
            return_year_with_halfyear(self.company.established_yr),
            attrs={'class':'form-control form-control-uniform'}
            )
        self.fields['product'].queryset = self.product
        self.fields['product'].empty_label = "Select Product"
        self.fields['half_year'].widget=forms.Select(choices=[('','Select Half Year'),
                                                            ('First_Half','First Half (July-Dec)'),
                                                            ('Second_Half','Second Half (Jan-June)')],
                                                            attrs={'disabled':'true','class':'form-control form-control-uniform'})

    class Meta:
        model=ProductionAndSalesPerformance
        fields = ('product','activity_year','half_year','production_amount','sales_amount','sales_value')
        widgets = {
            'product':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'production_amount':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_production_amount")'}),
            'sales_amount':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_sales_amount")'}),
            'sales_value':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_sales_value")'}),
        }

class AnualInputNeedForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        self.product = kwargs.pop('product')
        self.company = kwargs.pop('company')
        super(AnualInputNeedForm,self).__init__(*args,**kwargs)
        self.fields['year'].empty_label = "Select Year"
        self.fields['year'].widget = forms.Select(choices=
            return_year(self.company.established_yr),
            attrs={'class':'form-control form-control-uniform'}
            )
        self.fields['product'].queryset = self.product
        self.fields['product'].empty_label = "Select Product"
        self.fields['input_unit'].empty_label = "Select Unit of Measurement"

    class Meta:
        model=AnnualInputNeed
        fields = ('product','input_name','input_unit','year','is_active_input','amount','local_input','import_input')
        widgets = {
            'input_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Input Type'}),
            'product':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'is_active_input':forms.CheckboxInput(attrs={}),
            'amount':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("amount")'}),
            'local_input':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_local_input")'}),
            'import_input':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_import_input")'}),
        }

class InputDemandSupplyForm(forms.ModelForm):
    # year = forms.IntegerField(label="Year",widget=forms.Select(choices=return_year(),
    #             attrs={'class':'form-control form-control-uniform'}))
                # YEAR_CHOICES=[('','Select Year'),]
                # YEAR_CHOICES += [(r,r) for r in range(2000, datetime.date.today().year+1)]

    def __init__(self,*args,**kwargs):
        self.product = kwargs.pop('product')
        self.company = kwargs.pop('company')
        super(InputDemandSupplyForm,self).__init__(*args,**kwargs)
        self.fields['year'].empty_label = "Select Year"
        self.fields['year'].widget = forms.Select(choices=
            return_year_with_halfyear(self.company.established_yr),
            attrs={'class':'form-control form-control-uniform'}
            )
        self.fields['product'].queryset = self.product
        self.fields['product'].empty_label = "Select Product"
        self.fields['input_unit'].empty_label = "Select Unit of Measurement"
        self.fields['half_year'].widget=forms.Select(choices=[('','Select Half Year'),
                                                            ('First_Half','First Half (July-Dec)'),
                                                            ('Second_Half','Second Half (Jan-June)')],
                                                            attrs={'disabled':'true','class':'form-control form-control-uniform'})

    class Meta:
        model=InputDemandSupply
        fields = ('product','input_type','input_unit','year','half_year','demand','supply')
        widgets = {
            'input_type':forms.TextInput(attrs={'class':'form-control','placeholder':'Input Type '}),
            'product':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'demand':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_demand")'}),
            'supply':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_supply")'}),
        }


class ProductPriceForm(forms.ModelForm):
    class Meta:
        model = ProductPrice
        fields = ('price','startdate','end_date')
        widgets = {
            'price':forms.TextInput(attrs={'class':'form-control','placeholder':'Product Price',
                    'onkeyup':'isNumber("id_price")'}),
            'startdate':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'end_date':forms.DateInput(attrs={'class':'form-control','type':'date'})
        }

class ProductImageForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y = forms.FloatField(widget=forms.HiddenInput(),required=False)
    width = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height = forms.FloatField(widget=forms.HiddenInput(),required=False)
    
    class Meta:
        model = ProductImage
        fields = ('product_image',)
        widgets = {
            'product_image':forms.FileInput(attrs={'class':'form-control'})
        }

class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = (
            'rating','name','email','review'
        )
        widgets = {
            'rating':forms.TextInput(attrs={'type':'hidden'}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Your Name'}),
            'email':forms.EmailInput(attrs={'class':'form form-control','placeholder':'Your Email'}),
            'review':forms.Textarea(attrs={'class':'form-control','placeholder':'Your Message Here','row':'3'}),
        }

class ProductInquiryForm(forms.ModelForm):
    attacement = forms.FileField(required=False)
    class Meta:
        model = ProductInquiry
        fields = ("sender_email", "subject", "quantity","content", "attachement")
        widgets = {
            'sender_email':forms.TextInput(attrs={'class':'form-control','placeholder':'Your Email '}),
            'subject':forms.TextInput(attrs={'class':'form-control','placeholder':'subject '}),
            'quantity':forms.NumberInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'summernote form-control','placeholder':'Your inquiry content'}),
            'attachement':forms.FileInput(attrs={'class':'form-control'})
        }
        

