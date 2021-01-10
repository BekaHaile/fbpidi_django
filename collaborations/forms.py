from django import forms
from .models import PollsQuestion, Choices, PollsResult

class PollsForm(forms.ModelForm):
    
    class Meta:
        model = PollsQuestion
        fields = ('user','title', 'title_am',
                  'description', 'description_am')
        widgets = {
            'user':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Sub Category Name(English)'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Sub Category Name(Amharic)'}),
            'description_am':forms.Textarea(attrs={'class':'summernote'}),
          
        } 