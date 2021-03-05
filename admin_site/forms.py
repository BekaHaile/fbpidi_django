from django import forms

from admin_site.models import ChecklistMaster


class ChecklistMasterForm(forms.ModelForm):
    class Meta:
        model=ChecklistMaster
        fields = ('name','chk_type',)
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'CheckList Name'}),
            'chk_type':forms.Select(attrs={'class':'form-control form-control-uniform'}),
        }