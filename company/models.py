from django.db import models
from django.conf import settings
from admin_site.models import SubCategory


class Company(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    company_name = models.CharField(
        max_length=200, verbose_name="Company Name(English)")
    company_name_am = models.CharField(
        max_length=200, verbose_name="Company Name(Amharic)")
    location = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=20)
    detail = models.TextField(verbose_name="Company Detail(English)")
    detail_am = models.TextField(verbose_name="Company Detail(Amharic)")
    company_logo = models.ImageField(verbose_name="Company Logo",help_text="png,jpg,gif files, Max size 10MB")
    company_intro = models.FileField(verbose_name="Company Intro",default="",null=True,blank=True, help_text="mp4,mkv,avi files, Max size 10MB")
    company_type = models.CharField(max_length=255)
    company_type_am = models.CharField(max_length=255)
    number_of_employees = models.IntegerField(default=0,verbose_name="Number Of Employees")
    established_year= models.IntegerField(default=0,verbose_name="Established Year")
    certification = models.CharField(max_length=100,verbose_name="Certification")
    city = models.CharField(max_length=100,default="",verbose_name="City")
    postal_code = models.CharField(max_length=100,null=True,default="")
    product_category = models.ForeignKey(SubCategory,null=True,blank=True,on_delete=models.CASCADE,verbose_name="Main Products")
    capital = models.FloatField(default=0)
    color = models.CharField(default="#000000",max_length=10,verbose_name="Your Company Theme")
    facebook_link = models.CharField(max_length=100,default="",null=True,blank=True)
    twiter_link = models.CharField(max_length=100,default="",null=True,blank=True)
    google_link = models.CharField(max_length=100,default="",null=True,blank=True)
    pintrest_link = models.CharField(max_length=100,default="",null=True,blank=True)
    instagram_link = models.CharField(max_length=100,default="",null=True,blank=True)
    linkedin_link = models.CharField(max_length=100,default="",null=True,blank=True)
       # Trade Capacity
    incoterms = models.CharField(max_length=100,null=True,blank=True,verbose_name="International Commercial Terms(English)",help_text="Incoterms")
    incoterms_am  = models.CharField(max_length=100,null=True,blank=True,verbose_name="International Commercial Terms(Amharic)",help_text="Incoterms")
    average_lead_time  = models.CharField(max_length=100,null=True,blank=True,verbose_name="Average Lead Time(Amharic)")
    average_lead_time_am = models.CharField(max_length=100,null=True,blank=True,verbose_name="Average Lead Time(Amharic)")
    no_trading_staff = models.IntegerField(default=0,verbose_name="Number of Trading Staff")
    terms_of_payment = models.CharField(max_length=100,null=True,blank=True,verbose_name="Payment Method")
    export_yr = models.IntegerField(default=0,verbose_name="Export Year",null=True,blank=True)
    export_percentage = models.FloatField(default=0,verbose_name="Export Percentage",blank=True,null=True)
    main_market = models.CharField(max_length=100,null=True,blank=True,verbose_name="Main Market(English)")   
    main_market_am = models.CharField(max_length=100,null=True,blank=True,verbose_name="Main Market(Amharic)")                 
    nearest_port = models.CharField(max_length=100,null=True,blank=True,verbose_name='Nearest Port(English)')
    nearest_port_am = models.CharField(max_length=100,null=True,blank=True,verbose_name='Nearest Port(Amharic)')
    import_export = models.BooleanField(default=False)
        # production capacity
    r_and_d_capacity = models.CharField(max_length=100,null=True,blank=True,verbose_name='R&D Capacity(English)')
    r_and_d_capacity_am = models.CharField(max_length=100,null=True,blank=True,verbose_name='R&D Capacity(Amharic)')
    no_of_rnd_staff= models.IntegerField(default=0,null=True,blank=True,verbose_name='Number of R&D Staff')
    no_production_lines=models.IntegerField(default=0,null=True,blank=True,verbose_name='Number Of Production Lines')
    anual_op_value = models.CharField(max_length=100,null=True,blank=True,verbose_name='Anual Output Value')
    anual_op_main_products = models.TextField(verbose_name="Anual Output Value For Main Products(English)",blank=True,null=True)
    anual_op_main_products_am = models.TextField(verbose_name="Anual Output Value For Main Products(Amharic)",blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.company_name
    
    def get_image(self): 
        return self.company_logo.url if self.company_logo.url else None
        

    def get_bank_accounts(self):
        return self.companybankaccount_set.all() if self.companybankaccount_set.all().count() > 0 else None


class CompanyStaff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_company_name(self):
        return self.company.company_name if self.company.company_name else None

    def get_company(self):
        return Company.objects.get(user = self.user) if Company.objects.get(user = self.user) else None


class CompanySolution(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    title = models.CharField(max_length=200,verbose_name="Title(English)")
    title_am = models.CharField(max_length=200,verbose_name="Title(Amharic)")
    description = models.TextField(verbose_name="Description(English)")
    description_am = models.TextField(verbose_name="Description(Amharic)")
    link = models.CharField(verbose_name="link",max_length=200)
    image = models.ImageField()
    time_stamp = models.DateTimeField(auto_now_add=True)


class CompanyEvent(models.Model):
    EVENT_STATUS = [('Upcoming', 'Upcoming'),('Open', 'Open' ), ('Closed', 'Closed')]

    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    event_name = models.CharField(max_length=200,verbose_name="Event Name(English)")
    event_name_am = models.CharField(max_length=200,verbose_name="Event Name(Amharic)")
    description = models.TextField(verbose_name="Description(English)")
    description_am = models.TextField(verbose_name="Description(Amharic)")
    image = models.ImageField(blank = True, null = True)
    time_stamp = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(verbose_name="Event start date")
    end_date = models.DateTimeField(verbose_name="Event end date")
    status = models.CharField(max_length=10, verbose_name="Tender status", choices=EVENT_STATUS)


class EventParticipants(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(CompanyEvent, on_delete=models.CASCADE)
    patricipant_email = models.EmailField(max_length=200, blank=True)
    notifiy_in = models.IntegerField(default=1)
    notified = models.BooleanField(verbose_name="If notification is sent = True", default=False)

    class Meta:
        unique_together = (('patricipant_email', 'event'))
        


class Bank(models.Model):
    bank_name = models.CharField(verbose_name="bank name", max_length=255,)
    bank_name_am = models.CharField(verbose_name="bank name", max_length=255,default="")
    api_link = models.CharField(verbose_name="bank_api_link", max_length=255)

    def __str__(self):
        return self.bank_name


class CompanyBankAccount(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete = models.CASCADE)
    account_number = models.CharField(verbose_name="account number", max_length=30)

    def __str__(self):
        return f"{self.company.company_name}'s  {self.bank.bank_name} account"
    def get_bank_name(self):
        return f"{self.bank.bank_name}"

    class Meta:
        unique_together = (('company', 'bank','account_number'))