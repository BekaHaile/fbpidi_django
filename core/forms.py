from django import forms
from core.models import Faqs

class CreateFaqs(forms.ModelForm):
    
    answers = forms.CharField(required=True, widget=forms.Textarea(
    	attrs={'placeholder': 'answer'}))
    answers_am = forms.CharField(required=True,widget=forms.Textarea(
    	attrs={'placeholder': 'answer in amharic'}))
    questions    = forms.CharField(label='questions',widget=forms.TextInput(
    	attrs={'placeholder': 'question'}))
    questions_am = forms.CharField(label='questions_am',widget=forms.TextInput(
    	attrs={'placeholder': 'question in amharic'}))

    class Meta:
        model = Faqs
        fields = ('questions', 'questions_am',
                  'answers', 'answers_am')
    