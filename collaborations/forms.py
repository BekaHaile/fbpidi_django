from django.utils import timezone
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
    
from company.models import CompanyEvent, EventParticipants

from django.forms.widgets import SelectDateWidget

from PIL import Image

JOB_CHOICES=[ ('', 'Select Category'),
            ('Temporary','Temporary'),
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



def image_cropper(x,y,w,h,raw_image):
        # if the image is not cropped 
        if (x == '' or y == '' or w == '' or h == ''):
            image = Image.open(raw_image)
            resized_image = image.resize((600, 600), Image.ANTIALIAS)
            resized_image.save(raw_image.path)
            return True

        x = float(x)
        y = float(y)
        w = float(w)
        h = float(h)
        image = Image.open(raw_image)
        cropped_image = image.crop((x, y, w+x, h+y))
        ## replace the image with the cropped one
        cropped_image.save(raw_image.path)
        return True
   


class BlogsForm(forms.ModelForm):  

    tag = forms.MultipleChoiceField(choices = [ ('Food', 'Food'), ('Beverage', 'Beverage'), ('Pharmaceutical', 'Pharmaceutical')], required=True,  widget=forms.SelectMultiple(attrs={'type': 'dropdown','class':'form-control'}),) 
    tag_am = forms.MultipleChoiceField(choices = [ ('ምግብ', 'ምግብ'), ('መጠጥ', 'መጠጥ'), ('መድሀኒት', 'መድሀኒት')], required=True,widget=forms.SelectMultiple(attrs={'type': 'dropdown','class':'form-control'}),) 
    
    class Meta:
        model = Blog
        fields = ('blogImage','title', 'tag', 'content','publish','title_am','tag_am','content_am')
        widgets = {
                    'blogImage': forms.FileInput(attrs={'id': 'blogImage' ,'accept': 'image/*'}),
                    'content': forms.Textarea(attrs={'class':'summernote','placeholder':'Blog Content in English'}),
                    'content_am': forms.Textarea(attrs={'class':'summernote','placeholder':'Blog Content in Amharic'}),
                    'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of the Blog in English'}),
                    'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of the Blog in Amharic'})
                            }
    
    def save(self,user,company,x,y,w,h,tag_list,tag_list_am):
        blog = super(BlogsForm, self).save(commit=False)
        blog.created_by = user
        blog.company = company
        blog.tag = tag_list
        blog.tag_am = tag_list_am
        blog.save()

        ## if the image is not cropped 
        if (x == '' or y == '' or w == '' or h == ''):
            # just resize and save
            # change blog.blogImage with the image you want to resize 
            image = Image.open(blog.blogImage)
            resized_image = image.resize((600, 600), Image.ANTIALIAS)
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

    tag = forms.MultipleChoiceField(choices = [ ('Food', 'Food'), ('Beverage', 'Beverage'), ('Pharmaceutical', 'Pharmaceutical')], required=True,  widget=forms.SelectMultiple(attrs={'type': 'dropdown','class':'form-control'}),) 
    tag_am = forms.MultipleChoiceField(choices = [ ('ምግብ', 'ምግብ'), ('መጠጥ', 'መጠጥ'), ('መድሀኒት', 'መድሀኒት')], required=True,widget=forms.SelectMultiple(attrs={'type': 'dropdown','class':'form-control'}),) 

    class Meta:
        model = Blog
        fields = ('title', 'tag', 'content','publish','title_am','tag_am','content_am')
        widgets = {'content': forms.Textarea(attrs={'class':'summernote','placeholder':'Blog Content in English'}),
                    'content_am': forms.Textarea(attrs={'class':'summernote','placeholder':'Blog Content in Amharic'}),
                    'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of the Blog in English'}),
                    'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of the Blog in Amharic'}),
                    }
    def save(self,user,id,x,y,w,h,blog):
        blog_update = Blog.objects.get(id=id)
        blog_update.title = blog.title
        blog_update.title_am = blog.title_am
        blog_update.tag = blog.tag
        blog_update.tag_am = blog.tag_am
        blog_update.content =blog.content 
        blog_update.content_am =blog.content_am
        blog_update.publish = blog.publish
        blog_update.blogImage = blog.blogImage
        blog.last_updated_by = user
        blog.last_updated_date = timezone.now()
        blog_update.save()

         ## if the image is not cropped 
        if (x == '' or y == '' or w == '' or h == ''):
            # just resize and save
            # change blog.blogImage with the image you want to resize 
            image = Image.open(blog.blogImage)
            resized_image = image.resize((600, 600), Image.ANTIALIAS)
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
    
    class Meta:
        model = Tender
        fields = ('title', 'title_am','description', 'description_am' )
        widgets = {
                'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title English'}),
                'description':forms.Textarea(attrs={'class':'summernote','placeholder':'description of the Tender'}),
                'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title Amharic'}),
                'description_am':forms.Textarea(attrs={'class':'summernote','placeholder':'description of the Tender in amharic'}),
                }


class TenderApplicantForm(forms.Form):
    first_name= forms.CharField( max_length=30, widget=forms.TextInput(attrs={"id":"first_name", "class":"form-control","placeholder": "First Name", },)    )
    last_name=forms.CharField( max_length=30, widget=forms.TextInput(attrs={ "id":"last_name", "class":"form-control","placeholder": "Last Name", },)    )
    company_name= forms.CharField( max_length=30, widget=forms.TextInput(attrs={ "id":"company_name", "class":"form-control","placeholder": "Company Name", },)    )
    company_tin_number=forms.CharField( max_length=30, widget=forms.TextInput(attrs={"id":"company_tin_number",  "class":"form-control","placeholder": "Company tin Number", },)    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={ "id":"email", "class":"form-control","placeholder": "Email Address", },))   
    phone_number =  forms.IntegerField(widget=forms.TextInput(attrs={"id":"phone_number", "class":"form-control","placeholder": "Phone Number", "data-mask": "+251-99999-9999"},),)
            
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
    
    # employement_type = forms.ChoiceField(choices = JOB_CHOICES, required=True, widget=forms.Select(attrs={'type': 'dropdown','class':'form-control'}),)
    category= forms.ModelChoiceField(queryset = JobCategory.objects.all(), empty_label="Select Category", required = True, widget=forms.Select(attrs={'class':'form-control form-control-uniform'}))
    class Meta:
        model = Vacancy
        fields = ('location', 'salary', 'category'
                  ,'title', 'description','requirement',
                  'title_am','description_am','requirement_am', 'employement_type')
        
        widgets = {  
            'employement_type':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'location':forms.TextInput(attrs={'class':'form-control','placeholder':'Location'}),
            'salary':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("salary")','id':'salary','type':'number','placeholder':'Salary in Birr'}),
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Vacancy Title in English'}),
            'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Vacancy Title in Amharic'}),
            'description':forms.Textarea(attrs={'class':'summernote','placeholder':'Description in English'}),
            'description_am':forms.Textarea(attrs={'class':'summernote','placeholder':'Description in Amharic'}),
            'requirement':forms.Textarea(attrs={'class':'summernote','placeholder':'Requirements for the Job in English'}),
            'requirement_am':forms.Textarea(attrs={'class':'summernote','placeholder':'Requirements for the Job in Amharic'})
                      
        }

class CreateJobApplicationForm(forms.ModelForm):

    status = forms.ChoiceField(choices = CURRENT_STATUS, required=True, widget=forms.Select(attrs={'type': 'dropdown','class':'form-control'}),)
    
    class Meta:
        model = JobApplication
        fields = ('status', 'bio','cv', 'documents','experiance','grade','institiute','field') 
        
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
        fields = ('category_name','category_name_am')
        widgets ={
            'category_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Vacancy Category in English'}),
             'category_name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Vacancy Category in Amharic'}),
        }

class NewsForm(forms.ModelForm):
    # NEWS_CATAGORY = ( )
    NEWS_CATAGORY = [ ('', 'Select Category'),('Bevearage','Bevearage'),('Business','Business'), ('Food','Food'),('Job Related','Job Related'),('New Product Release','New Product Release'),('Pharmaceutical','Pharmaceutical'), ('Statistics','Statistics'), ('Technological','Technological')]
    catagory = forms.ChoiceField( required = True, choices= NEWS_CATAGORY, widget=forms.Select(attrs={'type': 'dropdown','class':'form-control'}),)
    image = forms.ImageField(allow_empty_file=True,  required=False, widget= forms.FileInput(attrs={'class': 'form-input-styled', 'id': "image_field"}) )
    class Meta:
        model = News
        fields = ('title', 'title_am', 'description', 'description_am', 'catagory','image')
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'News Title(English).'}),
            'title_am' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'News Title (Amharic).'}),
            'description':forms.Textarea(attrs={'class':'summernote','placeholder':'Detail description on the news.(English)'}),
            'description_am':forms.Textarea(attrs={'class':'summernote','placeholder':'Detail description on the news.(Amharic)'}),  
        } 

class CompanyEventForm(forms.ModelForm):
    STATUS_CHOICE = [ ('Upcoming', 'Upcoming'),('Open', 'Open' )]
    image = forms.ImageField(allow_empty_file=True,  required=False, widget= forms.FileInput(attrs={'class': 'form-input-styled', 'id': "image_field"}) )
    class Meta:
        model=CompanyEvent
        fields = ('title','title_am','description','description_am','image', 'start_date', 'end_date')
        widgets = {
            'title':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name (English)'}),
            'title_am':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name (Amharic)'}),
            'description': forms.Textarea(attrs={'class': 'summernote'}),
            'description_am': forms.Textarea(attrs={'class': 'summernote'}),
            'start_date': forms.DateTimeInput(attrs={'class':"form-control daterange-single"}),
            'end_date': forms.DateTimeInput(attrs={'class':"form-control daterange-single"}),
            
        }

class EventParticipantForm(forms.ModelForm):
    notify_on = forms.DateField(required=True, widget = forms.DateInput(attrs={'id':'notify_on', 'class':"form-control daterange-single", "name":"notify_on", "type":'date'}), )
    participant_email = forms.EmailField(required=True)
    class Meta:
        model=EventParticipants
        fields = ('patricipant_email', 'notify_on')
        widgets = {
        'patricipant_email': forms.EmailInput(attrs={'id':'participant_email', 'class': 'form-control', 'placeholder': 'Email Address..'}),
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
     
    class Meta:
        model = ForumComments
        fields = ('comment',)
        widgets = {
            'comment':forms.Textarea(attrs={'class':'form-control','placeholder':'Your Comment on the Forum'}),
        }

class CommentReplayForm(forms.ModelForm): 
    class Meta:
        model = CommentReplay
        fields = ('content',)
        widgets = {
            'content':forms.Textarea(attrs={'class':'form-control','placeholder':'Give your replay on the Forum comment'}),
        }
 
class AnnouncementForm(forms.ModelForm):

    class Meta:
        model = Announcement
        fields = ('title','title_am','description','description_am','image')
        widgets = {
        'image': forms.FileInput(attrs={'id': 'blogImage' ,'accept': 'image/*'}),
        'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of your Announcement in English'}),
        'title_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of your Announcement in Amharic'}),
        'description':forms.Textarea(attrs={'class': 'summernote','placeholder':'Discription of your Announcement in English'}),
        'description_am':forms.Textarea(attrs={'class': 'summernote','placeholder':'Discription of your Announcement in Amharic'}),
        
        }
    def save(self,x,y,w,h, user):
        announcement = super(AnnouncementForm, self).save(commit=False)
        announcement.created_by = user
        announcement.company = user.get_company()
        announcement.save()
        image_cropper(x,y,w,h,announcement.image)        
        return announcement

        
class ResearchProjectCategoryForm(forms.ModelForm):
    class Meta:
        model = ResearchProjectCategory
        fields = ('cateoryname','cateoryname_am')
        widgets = {
        'cateoryname':forms.TextInput(attrs={'class':'form-control','placeholder':'Category Name in English'}),
        'cateoryname_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Category Name in Amharic'}),
        
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
    # description = forms.CharField(widget=SummernoteWidget())
    # detail = forms.CharField(widget=SummernoteWidget())

    status = forms.ChoiceField(choices = (('','Select Status'),('Completed','Completed'),('Inprogress','Inprogress')), required=True, widget=forms.Select(attrs={'type': 'dropdown','class':'form-control'}),)
    category = forms.ModelChoiceField(queryset=ResearchProjectCategory.objects.all(), empty_label = "Select Research Category", required=True, widget =forms.Select(attrs={'class':'form-control form-control-uniform'}), )
    class Meta:
        model = Research
        fields  = ('title','description','status','category')
        widgets = {
        'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title of the Research'}),
        'description':forms.Textarea(attrs={'class':'summernote','placeholder':'Short description'}),
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
 

		






