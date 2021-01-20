from django import forms
from product import models
from admin_site.models import Category,SubCategory
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget



class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('category_type','category_name','category_name_am','description','description_am','image')
        widgets = {
            'image':forms.FileInput(attrs={'class':"form-control form-input-styled"}),
            'category_type':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'category_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Sub Category Name(English)'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'category_name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Sub Category Name(Amharic)'}),
            'description_am':forms.Textarea(attrs={'class':'summernote'}),
        }

class SubCategoryForm(forms.ModelForm):
    category_name = forms.ModelChoiceField(
        empty_label="Select Category Type",
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class':'form-control form-control-uniform'}),
        required=True
    )

    class Meta:
        model = SubCategory
        fields = ('category_name','sub_category_name','sub_category_name_am','description','description_am','image')
        widgets = {
            'image':forms.FileInput(attrs={'class':"form-control form-input-styled"}),
            # 'category_name':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'sub_category_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Sub Category Name(English)'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'sub_category_name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Sub Category Name(Amharic)'}),
            'description_am':forms.Textarea(attrs={'class':'summernote'}),
            # "description":SummernoteWidget(),
        } 

class ProductCreationForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        empty_label="Select Category",
        queryset=SubCategory.objects.all(),
        widget=forms.Select(attrs={'class':'form-control form-control-uniform'}),
        required=True
    )
    class Meta:
        model = models.Product
        fields = ('name','name_am','category','description','description_am','image',)
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Product Name(English)'}),
            'name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Product Name(Amharic)'}),
            # 'category':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'description_am':forms.Textarea(attrs={'class':'summernote'}),
            'image':forms.FileInput(attrs={'class':"form-control form-input-styled"})
        } 

# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = models.Review
#         fields = (
#             'rating','name','email','review'
#         )
#         widgets = {
#             'rating':forms.TextInput()
#         }