from django.db import models
from django.contrib.auth.models import Permission, Group

from django.conf import settings
from company.models import Company


class PollsQuestion(models.Model):
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    title = models.CharField( max_length=200, verbose_name="Poll title (English)" )
    title_am = models.CharField( max_length=200, verbose_name="Poll title(Amharic)" )
    description = models.TextField( verbose_name="Poll Description(English)" )
    description_am = models.TextField( verbose_name="Poll Description(Amharic)" )
    timestamp = models.DateTimeField(auto_now_add=True)
    choices = models.ManyToManyField('Choices',related_name='choices',default="",)
    
    
    def __str__(self):
        return self.title
    
    def count_votes(self):
        return self.pollsresult_set.count()
        
    def count_choices(self):
        return self.choices.count()
    
    def get_image(self):
        #gets the company by using the user, and in the company model there is a method called get_image() which returns image url
        if self.user.company_set.first():
            return self.user.company_set.first().get_image()
        else:
            return None
      
class Choices (models.Model):
    choice_name = models.CharField( max_length=200, verbose_name="Choice name (English)" )
    choice_name_am = models.CharField( max_length=200, verbose_name="Choice name(Amharic)" )
    description = models.TextField( verbose_name="Choice Description(English)" )
    description_am = models.TextField( verbose_name="Choice Description(Amharic)" )
    timestamp = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.choice_name

    def count_votes(self):
        return self.pollsresult_set.count()
    
    
class PollsResult(models.Model):    
    poll = models.ForeignKey(PollsQuestion, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choices, on_delete=models.CASCADE)
    remark = models.CharField( max_length=200,verbose_name= "Any remarks the user may have", default="" )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poll.title}'s Result "
    
    class Meta:
        unique_together = (('user', 'poll'))

## Colab 
class Blog(models.Model):
    title = models.CharField(max_length=100,null=False)
    title_am = models.CharField(max_length=100,null=False)
    tag = models.CharField(max_length=50,null=False)
    tag_am = models.CharField(max_length=50,null=False)
    blogImage = models.ImageField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    content_am = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(null=False,default=False)

            
    def countComment(self):
        return self.blogcomment_set.all().count()

    def comments(self):
        return self.blogcomment_set.all()
    
class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,null=False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=False)
    content = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

##Faqs
class Faqs(models.Model):
    questions = models.CharField(max_length=100,null=False)
    questions_am = models.TextField(max_length=100,null=False)  
    answers = models.TextField(null=False)  
    answers_am = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
 
class Tender(models.Model):
    TENDER_STATUS = ['Open', 'Panding', 'Closed', 'Suspended']
    

    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    title = models.CharField( max_length=200, verbose_name="Tender title (English)" )
    title_am = models.CharField( max_length=200, verbose_name="Tender title(Amharic)" )
    description = models.TextField( verbose_name="Tender Description(English)" )
    description_am = models.TextField( verbose_name="Tender Description(Amharic)" )
    tender_type = models.CharField(max_length=4, verbose_name="Tender type", choices=[ ('Free', 'Free'), ('Paid', 'Paid')], default="Free" )
    status = models.CharField(max_length=10, verbose_name="Tender status", choices=[
                                                                                        ('Pending', 'Pending'),('Open', 'Open' ), 
                                                                                        ('Closed', 'Closed'), ('Suspended', 'Suspended')
                                                                                    ])
    #if we r using the company logo there is no need to save it twice, we can get it from user.company.get_image()   
    #image = models.ImageField(verbose_name="Company image",help_text="png,jpg,gif files, Max size 10MB") 
    document = models.FileField(upload_to = "TenderDocuments/", max_length=254, verbose_name="Tender document",help_text="pdf, Max size 3MB", blank=True)
    bank_account = models.ManyToManyField('company.CompanyBankAccount', related_name="accounts")
    start_date = models.DateTimeField(verbose_name="Tender start date")
    end_date = models.DateTimeField(verbose_name="Tender end date")
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_applications(self):
        return TenderApplications.objects.filter( tender = self )
    
    def get_company(self):
        return Company.objects.get(user = self.user) if Company.objects.get(user = self.user) else None
    
    
        
       
class TenderApplicant(models.Model):
    first_name = models.CharField(verbose_name="first_name", max_length=50)
    last_name = models.CharField(verbose_name="first_name", max_length=50)
    phone_number = models.CharField(max_length=20,blank=True,null=True)
    email = models.EmailField(verbose_name="applicant email", max_length=255)
    company_name = models.CharField(verbose_name="first_name", max_length=50)
    company_tin_number = models.CharField(verbose_name="first_name", max_length=50)
   
    def __str__(self):
        return f"{self.first_name} {self.last_name} from {self.company_name}"
    
        

# This can be created automatically if we use a manytomanyrelation, that's why I commented this table and added a tender_applications
class TenderApplications(models.Model):
    applicant = models.ForeignKey(TenderApplicant, on_delete=models.CASCADE)
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('applicant', 'tender'))

        