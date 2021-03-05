from django import forms

from admin_site.models import CompanyDropdownsMaster,ProjectDropDownsMaster


class CompanyDropdownsMasterForm(forms.ModelForm):
    class Meta:
        model=CompanyDropdownsMaster
        fields = ('name','chk_type',)
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Company Lookup/Dropdown Name'}),
            'chk_type':forms.Select(attrs={'class':'form-control form-control-uniform'}),
        }
    
class ProjectDropdownsMasterForm(forms.ModelForm):
    class Meta:
        model=ProjectDropDownsMaster
        fields = ('name','dropdown_type',)
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Project Lookup/Dropdown Name'}),
            'dropdown_type':forms.Select(attrs={'class':'form-control form-control-uniform'}),
        }