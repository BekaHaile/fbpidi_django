from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import  (PollsQuestion, Choices, PollsResult,
                     Tender, TenderApplicant, 
                      JobCategory,Vacancy,JobApplication,
                      Faqs,Blog,BlogComment,
                      ForumQuestion,ForumComments,CommentReplay,
                      ForumComments,Announcement, News, NewsImages,
                      Research,Project,ResearchProjectCategory,
                      Document
                      )

from django.forms.widgets import SelectDateWidget

from PIL import Image

JOB_CHOICES=[('Temporary','Temporary'),
            ('Permanent','Permanent'),
            ('Contract','Contract')]

CURRENT_STATUS = [('JUST GRADUATED','JUST GRADUATED'),('WORKING','WORKING'),
                ('LOOKING FOR JOB','LOOKING FOR JOB')]

RESEARCH_STATUS = [('Completed','Completed'),('Inprogress','Inprogress'),]

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
        fields = ('blogImage','title', 'tag', 'content','publish','title_am','tag_am','content_am')
        widgets = {
                    'blogImage': forms.FileInput(attrs={'id': 'blogImage' ,'accept': 'image/*'}),
                    'content': forms.Textarea(attrs={'class':'summernote','placeholder':'Blog Content in English'}),
                    'content_am': forms.Textarea(attrs={'class':'summernote','placeholder':'Blog Content in Amharic'}),
                    'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of the Blog in English'}),
                    'tag':forms.TextInput(attrs={'class':'form-control','placeholder':'Tag in English'}),
                    'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of the Blog in Amharic'}),
                    'tag_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Tag in Amharic'}),
                    
                            }
    
    def save(self,user,x,y,w,h):
        blog = super(BlogsForm, self).save(commit=False)
        blog.user = user
        blog.save()

        ## if the image is not cropped 
        if (x == '' or y == '' or w == '' or h == ''):
            # just resize and save
            # change blog.blogImage with the image you want to resize 
            image = Image.open(blog.blogImage)
            resized_image = image.resize((w1, h1), Image.ANTIALIAS)
            resized_image.save(blog.blogImage.path)
            return blog

        x = float(x)
        y = float(y)
        w = float(w)
        h = float(h)
        # open the imaes about to be cropped
        # change blog.blogImage with the image you want to resize 
        image = Image.open(blog.blogImage)
        cropped_image = image.crop((x, y, w+x, h+y))
        #resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)

        ## replace the image with the cropped one
        cropped_image.save(blog.blogImage.path)
        return blog


class BlogsEdit(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ('title', 'tag', 'content','publish','title_am','tag_am','content_am')
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
        fields = ('title', 'title_am',
                  'description', 'description_am')
        widgets = {
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
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Poll Title English'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Poll Title Amharic'}),
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
    class Meta:
        model = Tender
        fields = ('title', 'title_am','description', 'description_am','tender_type',  )
        widgets = {
                'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title English'}),
                'description':forms.Textarea(attrs={'class':'summernote','placeholder':'description of the Tender'}),
                'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title Amharic'}),
                'description_am':forms.Textarea(attrs={'class':'summernote','placeholder':'description of the Tender in amharic'}),
                }

class TenderEditForm(forms.ModelForm):
    # user, bank_account, document
    tender_type = forms.ChoiceField(choices = [ ('Free', 'Free'), ('Paid', 'Paid')], required=True, widget=forms.RadioSelect(attrs={'type': 'radio'}),) 
    
    class Meta:
        model = Tender
        fields = ('title', 'title_am','description', 'description_am','tender_type')
        widgets = {
                'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title English'}),
                'description':forms.Textarea(attrs={'class':'summernote'}),
                'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title Amharic'}),
                'description_am':forms.Textarea(attrs={'class':'summernote'}),
            
            }


class TenderApplicantForm(forms.Form):
    first_name= forms.CharField( max_length=30, widget=forms.TextInput(attrs={ "class":"form-control","placeholder": "First Name", },)    )
    last_name=forms.CharField( max_length=30, widget=forms.TextInput(attrs={ "class":"form-control","placeholder": "Last Name", },)    )
    company_name= forms.CharField( max_length=30, widget=forms.TextInput(attrs={ "class":"form-control","placeholder": "Company Name", },)    )
    company_tin_number=forms.CharField( max_length=30, widget=forms.TextInput(attrs={ "class":"form-control","placeholder": "Company tin Number", },)    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={ "class":"form-control","placeholder": "Email Address", },))   
    phone_number =  forms.IntegerField(widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Phone Number", "data-mask": "+251-99999-9999"},),)
            
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
            'salary':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("salary")','id':'salary','type':'number','placeholder':'Salary in Birr'}),
            'job_title':forms.TextInput(attrs={'class':'form-control','placeholder':'Vacancy Title in English'}),
            'job_title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Vacancy Title in Amharic'}),
            'description':forms.Textarea(attrs={'class':'summernote','placeholder':'Description in English'}),
            'description_am':forms.Textarea(attrs={'class':'summernote','placeholder':'Description in Amharic'}),
            'requirement':forms.Textarea(attrs={'class':'summernote','placeholder':'Requirements for the Job in English'}),
            'requirement_am':forms.Textarea(attrs={'class':'summernote','placeholder':'Requirements for the Job in Amharic'})
                      
        }

class CreateJobApplicationForm(forms.ModelForm):

    status = forms.ChoiceField(choices = CURRENT_STATUS, required=True, widget=forms.Select(attrs={'type': 'dropdown','class':'form-control'}),)

    class Meta:
        model = JobApplication
        fields = ('status', 'bio',
                  'cv', 'documents','experiance',
                  'grade','institiute','field') 
        
        widgets = {
            'experiance':forms.TextInput(attrs={"placeholder": "2",'class':'form-control','onkeyup':'isNumber("experiance")','id':'experiance'},),
            'bio':forms.Textarea(attrs={'class':'summernote','placeholder':'Introduce your self and wright why you are appling'}),
            'institiute' : forms.TextInput(attrs={"placeholder": "school you learned in ",'class':'form-control'},),
            'field' : forms.TextInput(attrs={"placeholder": "The field you learned",'class':'form-control'},),
            'grade': forms.TextInput(attrs={"placeholder": "Your grade",'class':'form-control','onkeyup':'isNumber("grade")','id':'grade'},),
        }

class JobCategoryForm(forms.ModelForm):
    class Meta:
        model = JobCategory
        fields = ('categoryName','categoryName_am')
        widgets ={
            'categoryName':forms.TextInput(attrs={'class':'form-control','placeholder':'Cateory in English'}),
             'categoryName_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Category in Amharic'}),
        }

class NewsForm(forms.ModelForm):
    NEWS_CATAGORY = [ ('Bevearage','Bevearage'),('Business','Business'), ('Food','Food'),('Job Related','Job Related'),  
    ('New Product Release','New Product Release'),('Pharmaceutical','Pharmaceutical'), ('Statistics','Statistics'), ('Technological','Technological')]
    catagory = forms.ChoiceField(choices = NEWS_CATAGORY, required=True, widget=forms.Select(attrs={'type': 'dropdown'}),)

    class Meta:
        model = News
        fields = ('title', 'title_am', 'description', 'description_am', 'catagory')
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
            'content':forms.Textarea(attrs={'class':'form-control','placeholder':'Give your replay on the Forum comment'}),
        }

class AnnouncementForm(forms.ModelForm):

    class Meta:
        model = Announcement
        fields = ('title','title_am','description','description_am')
        widgets = {
        'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of your Announcement in English'}),
        'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of your Announcement in Amharic'}),
        'description':forms.Textarea(attrs={'class': 'summernote','placeholder':'Discription of your Announcement in English'}),
        'description_am':forms.Textarea(attrs={'class': 'summernote','placeholder':'Discription of your Announcement in Amharic'}),
        }
        
class ResearchProjectCategoryForm(forms.ModelForm):
    class Meta:
        model = ResearchProjectCategory
        fields = ('cateoryname','cateoryname_am','detail')
        widgets = {
        'cateoryname':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of the Cateory in English'}),
        'cateoryname_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of the Cateory in Amharic'}),
        'detail':forms.Textarea(attrs={'class':'form-control','placeholder':'detail description of the category'}),
        
        }  

class ProjectForm(forms.ModelForm):
    attachements = forms.FileField(required=False)
    # description = forms.CharField(widget=SummernoteWidget())
    # detail = forms.CharField(widget=SummernoteWidget())
    status = forms.ChoiceField(choices = RESEARCH_STATUS, required=True, widget=forms.Select(attrs={'type': 'dropdown','class':'form-control'}),)
    category = forms.ModelChoiceField( ResearchProjectCategory.objects.all(), empty_label="Select Category",required=True, widget=forms.Select(attrs={'class':'form-control form-control-uniform'}))
    class Meta:
        model = Project
        fields  = ('title','description','status','category')
        widgets = {
        # 'category':forms.Select(attrs={'class':'form-control form-control-uniform'}),
        'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of the Project'}),
        'description':forms.Textarea(attrs={'class':'summernote','placeholder':'Short description'}),
        }

class ResearchForm(forms.ModelForm):
    attachements = forms.FileField(required=False)
    # description = forms.CharField(widget=SummernoteWidget())
    # detail = forms.CharField(widget=SummernoteWidget())
    status = forms.ChoiceField(choices = RESEARCH_STATUS, required=True, widget=forms.Select(attrs={'type': 'dropdown','class':'form-control'}),)

    class Meta:
        model = Research
        fields  = ('title','description','detail','status','category')
        widgets = {

        'category':forms.Select(attrs={'class':'form-control form-control-uniform'}),
        'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of the Research'}),
        'description':forms.Textarea(attrs={'class':'summernote','placeholder':'Short description'}),
        'detail':forms.Textarea(attrs={'class':'summernote','placeholder':'The whole research'}),
        }
        
class DocumentForm(forms.ModelForm):
        document = forms.FileField( required=False )
        category = forms.ChoiceField( required = True,choices=Document.DOC_CATEGORY,  widget = forms.Select(attrs={'type':'dropdown', 'class':'form-control'}))

        class Meta:
            model = Document
            fields = ('title', 'category', 'document')
            widgets = {
                'title': forms.TextInput( attrs={'class': 'form-control form-control-uniform'}),
                'category': forms.Select( attrs={'type':'dropdown', 'class':'form-control'}),
                'document' : forms.FileInput( attrs={'class':'form-input-styled'})
            }
 

		






