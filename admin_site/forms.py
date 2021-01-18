from django import forms
<<<<<<< HEAD
=======
from admin_site import models
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class SubCategoryForm(forms.ModelForm):

    class Meta:
        model = models.SubCategory
        fields = ('category_name','sub_category_name','sub_category_name_am','description','description_am')
        widgets = {
            'category_name':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'sub_category_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Sub Category Name(English)'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'sub_category_name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Sub Category Name(Amharic)'}),
            'description_am':forms.Textarea(attrs={'class':'summernote'}),
            # "description":SummernoteWidget(),
        } 

class ProductCreationForm(forms.ModelForm):
    
    class Meta:
        model = models.Product
        fields = ('name','name_am','category','description','description_am','image',)
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Product Name(English)'}),
            'name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Product Name(Amharic)'}),
            'category':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'description_am':forms.Textarea(attrs={'class':'summernote'}),
            'image':forms.FileInput(attrs={'class':"form-control form-input-styled"})
        } 
>>>>>>> local/master
