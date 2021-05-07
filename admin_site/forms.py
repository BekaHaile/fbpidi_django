from django import forms

from admin_site.models import (CompanyDropdownsMaster,ProjectDropDownsMaster,
                                RegionMaster,UomMaster,PharmaceuticalProduct,
                                TherapeuticGroup)


class CompanyDropdownsMasterForm(forms.ModelForm):
    class Meta:
        model=CompanyDropdownsMaster
        fields = ('name','chk_type',)
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Company Lookup/Dropdown Name'}),
            'chk_type':forms.Select(attrs={'class':'form-control form-control-uniform'}),
        }

class RegionMasterForm(forms.ModelForm):
    class Meta:
        model=RegionMaster
        fields = ('name','name_am',)
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Region Name in English'}),
            'name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Region Name in Amharic'}),
        }

class UomMasterForm(forms.ModelForm):
    class Meta:
        model=UomMaster
        fields = ('name','name_am',)
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Unit of Measurement Short Name in English'}),
            'name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Unit of Measurement Short Name in Amharic'}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':'Unit of Measurement Full Name'}),
        }

class PharmaceuticalProductForm(forms.ModelForm):
    class Meta:
        model=PharmaceuticalProduct
        fields = ('name',)
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Pharmaceutical Product Group'}),
        }
        
class TherapeuticGroupForm(forms.ModelForm):
    class Meta:
        model=TherapeuticGroup
        fields = ('name',)
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Therapeutic Group Name'}),
        }

class ProjectDropdownsMasterForm(forms.ModelForm):
    class Meta:
        model=ProjectDropDownsMaster
        fields = ('name','dropdown_type',)
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Project Lookup/Dropdown Name'}),
            'dropdown_type':forms.Select(attrs={'class':'form-control form-control-uniform'}),
        }