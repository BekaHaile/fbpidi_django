from django import forms
from collaborations.models import Blog,BlogComment
from django_summernote.widgets import SummernoteWidget
from collaborations.models import Faqs
from .models import PollsQuestion, Choices, PollsResult, Tender, TenderApplicant, TenderApplications
from django.forms.widgets import SelectDateWidget

class CreateFaqs(forms.ModelForm):
    questions_am = forms.CharField(label='questions_am',widget=forms.TextInput(
    	attrs={'placeholder': 'question in amharic'}))

    class Meta:
        model = Faqs
        fields = ('questions', 'questions_am',
                  'answers', 'answers_am')
        widgets = {'answers': SummernoteWidget,'answers_am': SummernoteWidget}


class CreateBlogs(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ('title', 'tag', 'content','publish','blogImage','title_am','tag_am','content_am')
        widgets = {'content': SummernoteWidget,'content_am': SummernoteWidget}


class CreateBlogComment(forms.ModelForm):
	
	class Meta:
		model = BlogComment
		fields = ('content',)


class PollsForm(forms.ModelForm):
    
    class Meta:
        model = PollsQuestion
        fields = ('user','title', 'title_am',
                  'description', 'description_am','choices')
        widgets = {
            'user':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title in English'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title in Amharic'}),
            'description_am':forms.Textarea(attrs={'class':'summernote'}),
            
        }


class CreatePollForm(forms.ModelForm):
    class Meta:
        model = PollsQuestion
        fields = ('title', 'title_am',
                  'description', 'description_am',)
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title English'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title Amharic'}),
            'description_am':forms.Textarea(attrs={'class':'summernote'}),
           
        }


class CreateChoiceForm(forms.ModelForm):
    class Meta:
        model = Choices
        fields = ('choice_name', 'choice_name_am',
                  'description', 'description_am')
        
        widgets = {
            'choice_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Title English'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'choice_name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title Amharic'}),
            'description_am':forms.Textarea(attrs={'class':'summernote'}),          
        }

class TenderForm(forms.ModelForm):
    # user, bank_account, document
    tender_type = forms.ChoiceField(choices = [ ('Free', 'Free'), ('Paid', 'Paid')], required=True, widget=forms.RadioSelect(attrs={'type': 'radio'}),)
    status = forms.ChoiceField(choices = [ ('Pending', 'Pending'),('Open', 'Open' ),                                                                                         ('Closed', 'Closed'), ('Suspended', 'Suspended')
                                          ], required=True, widget=forms.Select(attrs={'type': 'dropdown'}),)
                                
    
    
    start_date = forms.DateTimeField( input_formats=['%d/%m/%Y %H:%M'],  widget=forms.DateTimeInput(attrs={
                                                                                'class': 'form-control datetimepicker-input', 'placeholder': 'dd/mm/YYYY HH:mm'}))

    end_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'],  widget=forms.DateTimeInput(attrs={
                                                                                'class': 'form-control datetimepicker-input', 'placeholder': 'dd/mm/YYYY HH:mm'}))
    class Meta:
        model = Tender
        fields = ('title', 'title_am','description', 'description_am','tender_type', 'status', 
                'start_date', 'end_date')
        widgets = {
                'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title English'}),
                'description':forms.Textarea(attrs={'class':'summernote'}),
                'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title Amharic'}),
                'description_am':forms.Textarea(attrs={'class':'summernote'}),
            
            }

class TenderEditForm(forms.ModelForm):
    # user, bank_account, document
    tender_type = forms.ChoiceField(choices = [ ('Free', 'Free'), ('Paid', 'Paid')], required=True, widget=forms.RadioSelect(attrs={'type': 'radio'}),)
    status = forms.ChoiceField(choices = [ ('Pending', 'Pending'),('Open', 'Open' ),                                                                                         ('Closed', 'Closed'), ('Suspended', 'Suspended')
                                          ], required=True, widget=forms.RadioSelect(attrs={'type': 'radio'}),)
                                
    
    
    class Meta:
        model = Tender
        fields = ('title', 'title_am','description', 'description_am','tender_type', 'status')
        widgets = {
                'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title English'}),
                'description':forms.Textarea(attrs={'class':'summernote'}),
                'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title Amharic'}),
                'description_am':forms.Textarea(attrs={'class':'summernote'}),
            
            }
