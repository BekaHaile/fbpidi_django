import datetime
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator


from company.models import Company,CompanyBankAccount


class PollsQuestion(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=2000, verbose_name="Poll title (English)")
    title_am = models.CharField(max_length=2000, verbose_name="Poll title(Amharic)")
    description = models.TextField(verbose_name="Poll Description(English)")
    description_am = models.TextField(verbose_name="Poll Description(Amharic)")
    choices = models.ManyToManyField('Choices',related_name='choices',default="")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT,null=True,blank=True,related_name="poll_updated_by")
    last_updated_date = models.DateTimeField(null=True)
    expired = models.BooleanField(default=False)

    
    model_am = "ምርጫዎች"

    def __str__(self):
        return self.title

    def save(self):
        self.company = self.created_by.get_company()
        super(PollsQuestion, self).save()
        
    def count_votes(self):
        return self.pollsresult_set.count()
        
    def count_choices(self):
        return self.choices.count()
    
    def get_company(self):
        return self.company
    
    def get_image(self):
        #gets the company by using the user, and in the company model there is a method called get_image() which returns image url
        return self.company.get_image()

    class Meta:
        ordering = ['-created_date',] 
    

class Choices (models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    choice_name = models.CharField( max_length=2000, verbose_name="Choice name (English)" )
    choice_name_am = models.CharField( max_length=2000, verbose_name="Choice name(Amharic)" )
    description = models.TextField( verbose_name="Choice Description(English)" )
    description_am = models.TextField( verbose_name="Choice Description(Amharic)" )
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT,null=True,blank=True,related_name="poll_choice_updated_by")
    last_updated_date = models.DateTimeField(null=True)
    expired = models.BooleanField(default=False)
    
    def __str__(self):
        return self.choice_name

    def count_votes(self):
        return self.pollsresult_set.count()

        
    class Meta:
        ordering = ['-created_date',] 


class PollsResult(models.Model):    
    poll = models.ForeignKey(PollsQuestion, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    choice = models.ForeignKey(Choices, on_delete=models.CASCADE)
    remark = models.CharField( max_length=200,verbose_name= "Any remarks the user may have", default="" )
    

    def __str__(self):
        return f"{self.poll.title}'s Result "
    
    def get_company(self):
        return user.get_company()
    
    class Meta:
        unique_together = (('user', 'poll'))

## Colab 
class Blog(models.Model):
    title = models.CharField(max_length=10000,null=False)
    title_am = models.CharField(max_length=10000,null=False)
    tag = models.CharField(max_length=500,null=False)
    tag_am = models.CharField(max_length=500,null=False)
    blogImage = models.ImageField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    content_am = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(null=False,default=False)

    model_am =  "ብሎጎች" 

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp',]
            
    def countComment(self):
        return self.blogcomment_set.all().count()

    def comments(self):
        return self.blogcomment_set.all()

class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,null=False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=False)
    content = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp',]


    def __str__(self):
        return self.title

##Faqs
class Faqs(models.Model):
    questions = models.CharField(max_length=10000,null=False)
    questions_am = models.TextField(max_length=10000,null=False)  
    answers = models.TextField(null=False)  
    answers_am = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100,null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-timestamp',]
    
    model_am = "በተደጋጋሚ የተጠየቁ ጥያቄዎች"


class Tender(models.Model):
    TENDER_STATUS = ['Open', 'Upcoming', 'Closed', 'Suspended']
    created_by = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    created_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey( Company, on_delete= models.CASCADE, default=1)
    title = models.CharField( max_length=200, verbose_name="Tender title (English)" )
    title_am = models.CharField( max_length=200, verbose_name="Tender title(Amharic)" )
    description = models.TextField( verbose_name="Tender Description(English)" )
    description_am = models.TextField( verbose_name="Tender Description(Amharic)" )
    document = models.FileField(upload_to = "TenderDocuments/", max_length=254, verbose_name="Tender document",help_text="pdf, Max size 3MB", blank=True)
    tender_type = models.CharField(max_length=4, verbose_name="Tender type", choices=[ ('Free', 'Free'), ('Paid', 'Paid')], default="Free" )
    document_price = models.FloatField(verbose_name="documnet price (for paid tenders)", max_length = 6, default=0)
    status = models.CharField(max_length=10, verbose_name="Tender status", choices=[
                                                                                        ('Upcoming', 'Upcoming'),('Open', 'Open' ), 
                                                                                        ('Closed', 'Closed'), ('Suspended', 'Suspended')
                                                                                    ])
    #if we r using the company logo there is no need to save it twice, we can get it from user.company.get_image()   
    #image = models.ImageField(verbose_name="Company image",help_text="png,jpg,gif files, Max size 10MB") 
    bank_account = models.ManyToManyField('company.CompanyBankAccount', related_name="accounts")
    start_date = models.DateTimeField(verbose_name="Tender start date")
    end_date = models.DateTimeField(verbose_name="Tender end date")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT,null=True,blank=True,related_name="tender_updated_by")
    last_updated_date = models.DateTimeField(null=True)
    expired = models.BooleanField(default=False)
    
    def get_applications(self):
        return TenderApplicant.objects.filter( tender = self )
    
    def get_company(self):
        return self.company
    
    model_am = "ጨረታዎች"
        
    def save(self):
        self.company = self.created_by.get_company()
        super(Tender, self).save()


    class Meta:
        ordering = ['-created_date',] 


class TenderApplicant(models.Model):
    first_name = models.CharField(verbose_name="first_name", max_length=50)
    last_name = models.CharField(verbose_name="first_name", max_length=50)
    phone_number = models.CharField(max_length=20,blank=True,null=True)
    email = models.EmailField(verbose_name="applicant email", max_length=255)
    company_name = models.CharField(verbose_name="first_name", max_length=50)
    company_tin_number = models.CharField(verbose_name="first_name", max_length=50)
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

  
    def __str__(self):
        return f"{self.first_name} {self.last_name} from {self.company_name}"
            
    class Meta:
        ordering = ['-timestamp',] 

## Vacancy
class JobCategory(models.Model):
    category_name = models.CharField(max_length=500,null=False)
    category_name_am = models.CharField(max_length=500,null=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


    def countjobs(self):
        return self.vacancy_set.filter(closed=False).count()

    def __str__(self):
        return self.category_name

    
class Vacancy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,related_name="company_vacancy")
    location = models.CharField(max_length=1000)
    salary = models.IntegerField(null=True,default=0)
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    employement_type = models.CharField(max_length=10000,null=False)
    starting_date = models.DateTimeField()
    ending_date = models.DateTimeField()
    job_title = models.CharField(max_length=10000,null=False)
    description = models.TextField(null=False)
    requirement = models.TextField(null=False)
    job_title_am = models.CharField(max_length=10000,null=False)
    description_am = models.TextField(null=False)
    requirement_am = models.TextField(null=False)
    closed = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT,null=True,blank=True,related_name="vacancy_created_by")
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT,null=True,blank=True,related_name="vacancy_updated_by")
    last_updated_date = models.DateTimeField(null=True)
    expired = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_date',]

    def __str__(self):
        return self.job_title

    def countApplicant(self):
        return self.jobapplication_set.all().count()
    
    def get_category_name(self):
        return self.category.category_name

    def get_company(self):
        return self.company

    model_am = "ክፍት የስራ ቦታዎች"


class JobApplication(models.Model):
    CURRENT_STATUS = [(('','Select Current Status'),'JUST GRADUATED','JUST GRADUATED'),('WORKING','WORKING'),
                ('LOOKING FOR JOB','LOOKING FOR JOB')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    institiute = models.CharField(max_length=500,null=False)
    grade = models.FloatField()
    field = models.CharField(max_length=500,null=False)
    status = models.CharField(max_length=500,null=False)
    bio = models.TextField(null=False)
    experiance = models.IntegerField(null=False)
    cv = models.FileField(upload_to="cv/", max_length=254,help_text="only pdf,jpg,doc,docx files, Max size 10MB",
            validators=[FileExtensionValidator(allowed_extensions=['pdf','jpg','doc','docx'])]
            )
    documents = models.FileField(upload_to="documents/", max_length=254,help_text="pdf, jpg,doc,docx files, Max size 10MB",
                                validators=[FileExtensionValidator(allowed_extensions=['pdf','jpg','doc','docx'])])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp',]
        unique_together = (('vacancy','user'))
    

## News and Events
class News(models.Model):
    NEWS_CATAGORY = [ ('Bevearage','Bevearage'),('Business','Business'), ('Food','Food'),('Job Related','Job Related'),  
    ('New Product Release','New Product Release'),('Pharmaceutical','Pharmaceutical'), ('Statistics','Statistics'), ('Technological','Technological')]

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default = 1)
    title = models.CharField(max_length=500, null = False)
    title_am = models.CharField(max_length=500, null = False)
    description = models.TextField( verbose_name="News Description(English)" )
    description_am = models.TextField( verbose_name="News Description(Amharic)" )
    catagory = models.TextField(verbose_name="News Catagory, the choices are ", choices=NEWS_CATAGORY)
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT,null=True,blank=True,related_name="news_updated_by")
    last_updated_date = models.DateTimeField(null=True)
    expired = models.BooleanField(default=False)

    model_am ="ዜናዎች"

    def get_images(self):
        return self.newsimages_set.all() if self.newsimages_set.exists() else None

    def get_single_image(self):
        return  self.newsimages_set.first().image.url 

    def get_company(self):
        return self.created_by.get_company()
    
    def save(self):
        self.company = self.created_by.get_company()
        super(News, self).save()

    class Meta:
        ordering = ['-created_date',] 
    


    
class NewsImages(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1, related_name='newsimages')
    created_date = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey(News, on_delete = models.CASCADE)
    name = models.CharField(verbose_name = "Image alternative name",max_length=255)
    image = models.ImageField(upload_to = "Images/News Images", max_length=254, verbose_name="News Image",help_text="jpg, png, gid", blank=False)  
    last_updated_by = models.ForeignKey (settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null = True, related_name="updated_newsimages")
    last_updated_date = models.DateTimeField(blank=True, null = True)
    expired = models.BooleanField(default=False)

    
    
    class Meta:
        ordering = ['-created_date',]

class ForumQuestion(models.Model):
    title = models.CharField(max_length=500,null=False)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    attachements = models.FileField(upload_to="Attachements/", null=True,max_length=254,help_text="only pdf files, Max size 10MB")
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp',]

    def countComment(self):
        return self.forumcomments_set.all().count()

    def comments(self):
        return self.forumcomments_set.all()
    
    model_am = "ውይይቶች"
    

class ForumComments(models.Model):
    forum_question=models.ForeignKey(ForumQuestion,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['-timestamp',]

    def count_comment_replays(self):
        return self.commentreplay_set.all().count()
    

    def commentreplay(self):
        return self.commentreplay_set.all()


class CommentReplay(models.Model):
    comment = models.ForeignKey(ForumComments,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-timestamp',]
    

class Announcement(models.Model):

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=500,null=False)
    title_am = models.CharField(max_length=500,null=False)
    description = models.TextField(null=False)
    description_am = models.TextField(null=False)
    last_updated_by = models.ForeignKey (settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null = True, related_name="announcemnt_updated")
    last_updated_date = models.DateTimeField(blank=True, null = True)
    expired = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_date',]

    def announcementimages(self):
        return self.announcementimages_set.all()
    
    def save(self):
        self.company = self.created_by.get_company()
        super(Announcement, self).save()
    
    model_am = "ማስታወቂያ"
    



class AnnouncementImages(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = "Announcements", max_length=254, verbose_name="Announcement Image",help_text="jpg, png, gid", blank=False)  
    created_date = models.DateTimeField(auto_now_add=True)
    expired = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_date',]



class ResearchProjectCategory(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    cateoryname = models.CharField(max_length=500,null=False)
    cateoryname_am = models.CharField(max_length=500,null=False)
    detail = models.TextField(null=False)
    last_updated_by = models.ForeignKey (settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null = True, related_name="category_updated")
    last_updated_date = models.DateTimeField(blank=True, null = True)
    expired = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_date',]

    def __str__(self):
        return self.cateoryname

    def countResearch(self):
        return self.research_set.all().count()

    def countProject(self):
        return self.project_set.all().count()

    def Researchs(self):
        return self.research_set.all()
    
    


class Research(models.Model):
    title = models.CharField(max_length=500,null=False)
    description = models.TextField(null=False)
    status = models.CharField(max_length=100,null=False)
    accepted = models.CharField(max_length=100,null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(ResearchProjectCategory, on_delete = models.CASCADE)
    
    class Meta:
        ordering = ['-timestamp',]

    def researchfiles(self):
        return self.researchattachment_set.all()
    
    def get_category_name(self):
        return self.category.cateoryname
    
    model_am = "ምርምር"

class ResearchAttachment(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    attachement = models.FileField(upload_to="ResearchAttachements/",null=True, max_length=254,help_text="only pdf files, Max size 10MB")
    timestamp = models.DateTimeField(auto_now_add=True)


class Project(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=500,null=False)
    description = models.TextField(null=False)
    status = models.CharField(max_length=100,null=False)
    category = models.ForeignKey(ResearchProjectCategory, on_delete = models.CASCADE)
    attachements = models.FileField(upload_to="ProjectAttachements/",null=True, max_length=254,help_text="only pdf files, Max size 10MB")
    last_updated_by = models.ForeignKey (settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null = True, related_name="project_updated")
    last_updated_date = models.DateTimeField(blank=True, null = True)
    expired = models.BooleanField(default=False)


    class Meta:
        ordering = ['-created_date',]

    def save(self):
        self.company = self.created_by.get_company()
        super(Project,self).save()
    
    def get_category_name(self):
        return self.category.cateoryname
    model_am =  "ፕሮጀክት"

class Document_Category(models.Model):
    
    title = models.CharField(max_length=250, verbose_name="category title", help_text="category name for documents.")
    description = models.CharField(max_length = 250, verbose_name = "category description", help_text="some detail information about the category")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank=True, null=True) # if it is null then the category is created by the system
    created_date = models.DateTimeField(auto_now_add=True)


class Document(models.Model):
    DOC_CATEGORY = [ ('Company Forms', 'Company Forms'), ('Finance','Finance'),('HR', 'HR'), ('Managment','Managment'),]

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(verbose_name="upload time", auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=250, verbose_name="document title")
    document = models.FileField(upload_to="Documents/", blank="False")
    category = models.CharField( max_length = 250, choices=DOC_CATEGORY)
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT,null=True,blank=True,related_name="document_updated_by")
    last_updated_date = models.DateTimeField(null=True)
    expired = models.BooleanField(default=False)

    def save(self):
        self.company = self.created_by.get_company()
        super(Document, self).save()
    
    class Meta:
        ordering = ['-created_date']
