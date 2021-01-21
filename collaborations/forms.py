from django import forms
from django_summernote.widgets import SummernoteWidget
from collaborations.models import Faqs
from collaborations.models import Faqs,Blog,BlogComment,Vacancy,JobApplication
from .models import  PollsQuestion, Choices, PollsResult, Tender, TenderApplicant, TenderApplications, JobCategoty
from django.forms.widgets import SelectDateWidget


JOB_CHOICES=[('Temporary','Temporary'),
            ('Permanent','Permanent'),
            ('Contract','Contract')]

class FaqsForm(forms.ModelForm):
    

    class Meta:
        model = Faqs
        fields = ('questions', 'questions_am',
                  'answers', 'answers_am')
        widgets = {'answers': forms.Textarea(attrs={'class':'summernote'}),
                    'answers_am': forms.Textarea(attrs={'class':'summernote'}),
                    'questions':forms.TextInput(attrs={'class':'form-control'}),
                    'questions_am':forms.TextInput(attrs={'class':'form-control'})}

class BlogsForm(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ('title', 'tag', 'content','publish','blogImage','title_am','tag_am','content_am')
        widgets = {'content': forms.Textarea(attrs={'class':'summernote'}),
                    'content_am': forms.Textarea(attrs={'class':'summernote'}),
                    'title':forms.TextInput(attrs={'class':'form-control'}),
                    'tag':forms.TextInput(attrs={'class':'form-control'}),
                    'title_am':forms.TextInput(attrs={'class':'form-control'}),
                    'tag_am':forms.TextInput(attrs={'class':'form-control'}),


                            }


class BlogCommentForm(forms.ModelForm):
	
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
    STATUS_CHOICE = [ ('Pending', 'Pending'),('Open', 'Open' )]
    tender_type = forms.ChoiceField(choices = [ ('Free', 'Free'), ('Paid', 'Paid')], required=True, widget=forms.RadioSelect(attrs={'type': 'radio'}),)
    status = forms.ChoiceField(choices = STATUS_CHOICE, required=True, widget=forms.Select(attrs={'type': 'dropdown'}),)
                                
    
    
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
    status = forms.ChoiceField(choices = [ ('Pending', 'Pending'),('Open', 'Open' ),  ('Closed', 'Closed'), ('Suspended', 'Suspended')
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



'''
class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    ) 
'''

class VacancyForm(forms.ModelForm):

    employement_type = forms.CharField(label='job type', widget=forms.Select(choices=JOB_CHOICES))
    starting_date = forms.DateField(widget=SelectDateWidget())

    ending_date = forms.DateField(widget=SelectDateWidget())

    class Meta:
        model = Vacancy
        fields = ('location', 'salary', 'category'
                  ,'job_title', 'description','requirement',
                  'job_title_am','description_am','requirement_am')
        
        widgets = {
            'category':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'location':forms.TextInput(attrs={'class':'form-control','placeholder':'Location'}),
            'job_title':forms.TextInput(attrs={'class':'form-control'}),
            'job_title_am':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'description_am':forms.Textarea(attrs={'class':'summernote'}),
            'requirement':forms.TextInput(attrs={'class':'form-control','placeholder':'Requirement'}),
            'requirement_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Requirement in Amharic'})
                      
        }



class CreateJobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ('status', 'bio',
                  'cv', 'documents') 
        
        widgets = {
            'status':forms.TextInput(attrs={'class':'form-control','placeholder':'Current employement status'}),
            'bio':forms.Textarea(attrs={'class':'summernote'}),         
        }

class JobCategoryForm(forms.ModelForm):
    class Meta:
        model = JobCategoty
        fields = ('categoryName','categoryName_am')
        widgets ={
            'categoryName':forms.TextInput(attrs={'class':'form-control','placeholder':'Title English'}),
             'categoryName_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title Amharic'}),
        }



