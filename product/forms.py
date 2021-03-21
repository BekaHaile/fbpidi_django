import datetime

from django import forms
from django.db.transaction import atomic

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from PIL import Image

from product.models import *
from admin_site.models import Category
from company.models import SubCategory,Company,Brand



class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('category_type','category_name','category_name_am','description','description_am','icons')
        widgets = {
            'icons':forms.FileInput(attrs={'class':"form-control form-input-styled"}),
            'category_type':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'category_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Sub Category Name(English)'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'category_name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Sub Category Name(Amharic)'}),
            'description_am':forms.Textarea(attrs={'class':'summernote'}),
        }

class BrandForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.company = kwargs.pop('company')
        super(BrandForm,self).__init__(*args,**kwargs)
        self.fields['product_type'].empty_label = "Select A Product Type"
        self.fields['product_type'].queryset = SubCategory.objects.filter(company=self.company)
        
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
        self.company = kwargs.pop('company')
        super(SubCategoryForm,self).__init__(*args,**kwargs)
        self.fields['category_name'].queryset = self.company.category.all()
        self.fields['category_name'].empty_label = "Select A Product Category"

   

    class Meta:
        model = SubCategory
        fields = ('category_name','sub_category_name','sub_category_name_am','description','description_am','icons')
        widgets = {
            'icons':forms.FileInput(attrs={'class':"form-control form-input-styled"}),
            # 'category_name':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'sub_category_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Sub Category Name(English)'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'sub_category_name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Sub Category Name(Amharic)'}),
            'description_am':forms.Textarea(attrs={'class':'summernote'}),
            # "description":SummernoteWidget(),
        } 

class ProductCreationForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y = forms.FloatField(widget=forms.HiddenInput(),required=False)
    width = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height = forms.FloatField(widget=forms.HiddenInput(),required=False)

    def __init__(self,*args,**kwargs):
        self.company = kwargs.pop('company')
        super(ProductCreationForm,self).__init__(*args,**kwargs)
        self.fields['fandb_category'].queryset = Brand.objects.filter(company=self.company)
        if self.company.main_category == 'FBPIDI':
             self.fields['pharmacy_category'].queryset = Category.objects.filter(category_type="Pharmaceuticals")
        else:
            self.fields['pharmacy_category'].queryset = Category.objects.filter(category_type=self.company.main_category)
        self.fields['dose'].queryset = Dose.objects.all()
        self.fields['dosage_form'].queryset = DosageForm.objects.all()
        self.fields['dose'].empty_label = "Select Prodect Dose"
        self.fields['dosage_form'].empty_label = "Select Product Dosage Form"
        self.fields['fandb_category'].empty_label = "Select Product Brand"
        self.fields['pharmacy_category'].empty_label = "Select Product Category"
     
    class Meta:
        model = Product
        fields = ('name','name_am','fandb_category','pharmacy_category',
                    'dose','dosage_form','uom','quantity','therapeutic_group',
                    'description','description_am','image',)
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Product Name(English)'}),
            'name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Product Name(Amharic)'}),
            'fandb_category':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'pharmacy_category':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'dose':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'dosage_form':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'therapeutic_group':forms.TextInput(attrs={'class':'form-control','placeholder':'Therapeutic Group'}),
            'description':forms.Textarea(attrs={'class':'summernote','required':'False'}),
            'description_am':forms.Textarea(attrs={'class':'summernote','required':'False'}),
            'image':forms.FileInput(attrs={'class':"form-control form-input-styled"}),
            'uom':forms.TextInput(attrs={'class':'form-control','placeholder':'Unit Of Measurement'}),
            'quantity':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_quantity")'}),
        } 

    @atomic
    def save(self,commit=True):
        product = super(ProductCreationForm, self).save(commit=commit)

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        if (x or y or w or h ):
                image = Image.open(product.image)
                cropped_image = image.crop((x, y, w+x, h+y))
                resized_image = cropped_image.resize((1280, 720), Image.ANTIALIAS)
                resized_image.save(product.image.path)

                return product
                
        else:
                image = Image.open(product.image)
                resized_image = image.resize((1280, 720), Image.ANTIALIAS)
                resized_image.save(product.image.path)
                return product
    


class DosageFormForm(forms.ModelForm):
    class Meta:
        model = DosageForm
        fields = ('dosage_form','dosage_form_am','description','description_am',)
        widgets = {
            'dosage_form':forms.TextInput(attrs={'class':'form-control','placeholder':'Dosage Form in English'}),
            'dosage_form_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Dosage Form in Amharic'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'description_am':forms.Textarea(attrs={'class':'summernote'})

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
    class Meta:
        model=ProductionCapacity
        fields = ('p_date','install_prdn_capacity','atnbl_prdn_capacity',
                    'actual_prdn_capacity','production_plan','extraction_rate')
        widgets = {
            'p_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'install_prdn_capacity':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_install_prdn_capacity")'}),
            'atnbl_prdn_capacity':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_atnbl_prdn_capacity")'}),
            'actual_prdn_capacity':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_actual_prdn_capacity")'}),
            'production_plan':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_production_plan")'}),
            'extraction_rate':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_extraction_rate")'}),
        }

class ProductPackagingForm(forms.ModelForm):
    class Meta:
        model=ProductPackaging
        fields = ('packaging','category','amount','local_input','import_input','wastage')
        widgets = {
            'packaging':forms.TextInput(attrs={'class':'form-control','placeholder':'Packaging Type'}),
            'category':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'amount':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_amount")'}),
            'local_input':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_local_input")'}),
            'import_input':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_import_input")'}),
            'wastage':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_wastage")'}),
        }
YEAR_CHOICES=[('','Select Year'),]
YEAR_CHOICES += [(r,r) for r in range(2000, datetime.date.today().year+1)]

class SalesPerformanceForm(forms.ModelForm):
    activity_year = forms.IntegerField(label="Activity Year",widget=forms.Select(choices=YEAR_CHOICES,
                attrs={'class':'form-control form-control-uniform'}))

    def __init__(self,*args,**kwargs):
        super(SalesPerformanceForm,self).__init__(*args,**kwargs)
        self.fields['activity_year'].choices = YEAR_CHOICES

    class Meta:
        model=ProductionAndSalesPerformance
        fields = ('activity_year','production_amount','sales_amount','sales_value')
        widgets = {
            'activity_year':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'production_amount':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_production_amount")'}),
            'sales_amount':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_sales_amount")'}),
            'sales_value':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_sales_value")'}),
        }

class AnualInputNeedForm(forms.ModelForm):
    year = forms.IntegerField(label="Year",widget=forms.Select(choices=YEAR_CHOICES,
                attrs={'class':'form-control form-control-uniform'}))

    def __init__(self,*args,**kwargs):
        super(AnualInputNeedForm,self).__init__(*args,**kwargs)
        self.fields['year'].get_queryset = YEAR_CHOICES

    class Meta:
        model=AnnualInputNeed
        fields = ('input_name','year','is_active_input','amount','local_input','import_input')
        widgets = {
            'input_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Input Type'}),
            'year':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'is_active_input':forms.CheckboxInput(attrs={}),
            'amount':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("amount")'}),
            'local_input':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_local_input")'}),
            'import_input':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_import_input")'}),
        }

class InputDemandSupplyForm(forms.ModelForm):
    year = forms.IntegerField(label="Year",widget=forms.Select(choices=YEAR_CHOICES,
                attrs={'class':'form-control form-control-uniform'}))
    def __init__(self,*args,**kwargs):
        self.product = kwargs.pop('product')
        super(InputDemandSupplyForm,self).__init__(*args,**kwargs)
        self.fields['year'].queryset = YEAR_CHOICES
        self.fields['input_type'].queryset = AnnualInputNeed.objects.filter(product=self.product)
        self.fields['input_type'].empty_label = "Select Input Type"

    class Meta:
        model=InputDemandSupply
        fields = ('input_type','year','demand','supply')
        widgets = {
            'input_type':forms.Select(attrs={'class':'form-control'}),
            'year':forms.Select(attrs={'class':'form-control form-control-uniform'}),
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
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':'Your Email'}),
            'review':forms.Textarea(attrs={'class':'form-control','placeholder':'Your Message Here','row':'3'}),
        }


class CheckoutForm(forms.ModelForm):
    class Meta:
        model=ShippingAddress
        fields = ('first_name','last_name','company','city','email',
                  'street_address','home_address','phone_no',)
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Your First Name',}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Your Last Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Your Email Address Here'}),
            'phone_no':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number'}),
            'company':forms.TextInput(attrs={'class':'form-control','placeholder':'Your Company (optional)'}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':'Your City '}),
            'street_address':forms.TextInput(attrs={'class':'form-control','placeholder':'Street Address'}),
            'home_address':forms.TextInput(attrs={'class':'form-control','placeholder':'Home Address'}),
        }
    