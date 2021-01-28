from django import forms
from django_summernote.widgets import SummernoteWidget
from collaborations.models import Faqs,Blog,BlogComment,Vacancy,JobApplication
# from .models import  PollsQuestion, Choices, PollsResult, Tender, TenderApplicant, TenderApplications, JobCategoty, 
from .models import  (PollsQuestion, Choices, PollsResult,
                     Tender, TenderApplicant, TenderApplications,
                      JobCategoty,Vacancy,JobApplication,
                      Faqs,Blog,BlogComment,
                      ForumQuestion,ForumComments,CommentReplay,
                      ForumComments,Announcement, News, NewsImages
                      )

from django.forms.widgets import SelectDateWidget


JOB_CHOICES=[('Temporary','Temporary'),
            ('Permanent','Permanent'),
            ('Contract','Contract')]

CURRENT_STATUS = [('JUST GRADUATED','JUST GRADUATED'),('WORKING','WORKING'),
                ('LOOKING FOR JOB','LOOKING FOR JOB')]

class FaqsForm(forms.ModelForm):
    

    class Meta:
        model = Faqs
        fields = ('questions', 'questions_am',
                  'answers', 'answers_am')
        widgets = {'answers': forms.Textarea(attrs={'class':'summernote','placeholder':'Answer '}),
                    'answers_am': forms.Textarea(attrs={'class':'summernote','placeholder':'Answer in amharic'}),
                    'questions':forms.TextInput(attrs={'class':'form-control','placeholder':'The Frequently asked Question '}),
                    'questions_am':forms.TextInput(attrs={'class':'form-control','placeholder':'The Frequently asked Question in Amharic'})}

class BlogsForm(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ('title', 'tag', 'content','publish','blogImage','title_am','tag_am','content_am')
        widgets = {'content': forms.Textarea(attrs={'class':'summernote','placeholder':'Blog Content in English'}),
                    'content_am': forms.Textarea(attrs={'class':'summernote','placeholder':'Blog Content in Amharic'}),
                    'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of the Blog in English'}),
                    'tag':forms.TextInput(attrs={'class':'form-control','placeholder':'Tag in English'}),
                    'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of the Blog in Amharic'}),
                    'tag_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Tag in Amharic'}),


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
            'description':forms.Textarea(attrs={'class':'summernote','placeholder':'Description in English'}),
            'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title in Amharic'}),
            'description_am':forms.Textarea(attrs={'class':'summernote','placeholder':'Description in Amharic'}),
            
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


    class Meta:
        model = Tender
        fields = ('title', 'title_am','description', 'description_am','tender_type', 'status', )
        widgets = {
                'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title English'}),
                'description':forms.Textarea(attrs={'class':'summernote','placeholder':'description of the Tender'}),
                'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title Amharic'}),
                'description_am':forms.Textarea(attrs={'class':'summernote','placeholder':'description of the Tender in amharic'}),
            
            }

class TenderEditForm(forms.ModelForm):
    # user, bank_account, document
    tender_type = forms.ChoiceField(choices = [ ('Free', 'Free'), ('Paid', 'Paid')], required=True, widget=forms.RadioSelect(attrs={'type': 'radio'}),)
    status = forms.ChoiceField(choices = [ ('Pending', 'Pending'),('Open', 'Open' ),  ('Closed', 'Closed'), ('Suspended', 'Suspended')
                                          ], required=True,)
                                
    
    
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
    
    employement_type = forms.ChoiceField(choices = JOB_CHOICES, required=True, widget=forms.Select(attrs={'type': 'dropdown','class':'form-control'}),)

    class Meta:
        model = Vacancy
        fields = ('location', 'salary', 'category'
                  ,'job_title', 'description','requirement',
                  'job_title_am','description_am','requirement_am')
        
        widgets = {  
            #'employement_type':forms.Select(attrs={'class':'form-control form-control-uniform','choices':JOB_CHOICES}),
            'category':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'location':forms.TextInput(attrs={'class':'form-control','placeholder':'Location'}),
            'salary':forms.TextInput(attrs={'class':'form-control','type':'number','placeholder':'Salary in Birr'}),
            'job_title':forms.TextInput(attrs={'class':'form-control','placeholder':'Job Title in English'}),
            'job_title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Job Title in Amharic'}),
            'description':forms.Textarea(attrs={'class':'summernote','placeholder':'Description in English'}),
            'description_am':forms.Textarea(attrs={'class':'summernote','placeholder':'Description in Amharic'}),
            'requirement':forms.TextInput(attrs={'class':'form-control','placeholder':'Requirements for the Job in English'}),
            'requirement_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Requirements for the Job in Amharic'})
                      
        }



class CreateJobApplicationForm(forms.ModelForm):

    status = forms.ChoiceField(choices = CURRENT_STATUS, required=True, widget=forms.Select(attrs={'type': 'dropdown','class':'form-control'}),)

    class Meta:
        model = JobApplication
        fields = ('status', 'bio',
                  'cv', 'documents') 
        
        widgets = {
            
            'bio':forms.Textarea(attrs={'class':'summernote','placeholder':'Introduce your self and wright why you are appling'}),         
        }

class JobCategoryForm(forms.ModelForm):
    class Meta:
        model = JobCategoty
        fields = ('categoryName','categoryName_am')
        widgets ={
            'categoryName':forms.TextInput(attrs={'class':'form-control','placeholder':'Cateory in English'}),
             'categoryName_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Category in Amharic'}),
        }

class NewsForm(forms.ModelForm):
   
    class Meta:
        model = News
        fields = ('title', 'title_am', 'description', 'description_am')
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'News Title(English).'}),
            'title_am' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'News Title (Amharic).'}),
            'description':forms.Textarea(attrs={'class':'summernote','placeholder':'Detail description on the news.(English)'}),
            'description_am':forms.Textarea(attrs={'class':'summernote','placeholder':'Detail description on the news.(Amharic)'}),
            
        } 

class ForumQuestionForm(forms.ModelForm):
    attachements = forms.FileField(required=False)

    class Meta:
        model = ForumQuestion
        fields = ('title','description',)
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of your Forum Question'}),
            'description':forms.Textarea(attrs={'class': 'summernote','placeholder':'Elaborate your question'}),
        }               

class CommentForm(forms.ModelForm):
    
    attachements = forms.FileField(required=False)
    class Meta:
        model = ForumComments
        fields = ('comment',)
        widgets = {
            'comment':forms.Textarea(attrs={'class':'form-control','placeholder':'Your Comment on the Forum'}),
        }

class CommentReplayForm(forms.ModelForm):
    attachements = forms.FileField(required=False)
    class Meta:
        model = CommentReplay
        fields = ('content',)
        widgets = {
            'content':forms.Textarea(attrs={'class':'form-control','placeholder':'Your Comment on the Forum'}),
        }

class AnnouncementForm(forms.ModelForm):

    class Meta:
        model = Announcement
        fields = ('title','title_am','containt','containt_am')
        widgets = {
        'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of your Announcement in English'}),
        'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of your Announcement in Amharic'}),
        'containt':forms.Textarea(attrs={'class': 'summernote','placeholder':'Discription of your Announcement in English'}),
        'containt_am':forms.Textarea(attrs={'class': 'summernote','placeholder':'Discription of your Announcement in Amharic'}),

        }











