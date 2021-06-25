
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import ContentType

CAT_LIST = (
    ('','Select Sector'),
    ("Food",'Food'),
    ("Beverage",'Beverages'),
    ("Pharmaceuticals",'Pharmaceuticals'),
)

CAT_LIST_AM = (
    ('','ሴክተር ይምረጡ'),
    ("ምግብ",'ምግብ'),
    ("መጠጥ",'መጠጥ'),
    ("ፋርማሲ",'Pharmaceuticals'),
)

class Category(models.Model): #Sub sectors (cereal and pulses)
    category_type = models.CharField(choices=CAT_LIST,max_length=200,verbose_name="Sector Name(English)")
    category_type_am = models.CharField(choices=CAT_LIST,max_length=200,verbose_name="Sector Sector(Amharic)")
    category_name = models.CharField(max_length=200,verbose_name="Sub Sector Name(English)")
    category_name_am = models.CharField(max_length=200,verbose_name="Sub Sector Name(Amharic)")
    description = models.TextField(verbose_name="Description(English)",default="")
    description_am = models.TextField(verbose_name="Description(Amharic)",default="")
    icons = models.ImageField()
    created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='category_created_by',null=True)
    created_date	= models.DateTimeField(auto_now_add=True)
    last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='category_updated_by',null=True)
    last_updated_date	= models.DateTimeField(null=True)
    expired	= models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=False)
    

    def __str__(self):
        return self.category_name
    
    class Meta:
        ordering = ('category_name',)


# class CategoryProduct(models.Model):
#     category_type = models.ForeignKey(SubCategory,on_delete=models.RESTRICT,verbose_name="Category")
#     name = models.CharField(max_length=200,verbose_name="Category Product Name(English)")
#     name_am = models.CharField(max_length=200,verbose_name="Category Product Name(Amharic)")
#     created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='cat_product_created_by',null=True)
#     created_date	= models.DateTimeField(auto_now_add=True)
#     last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='cat_product_updated_by',null=True)
#     last_updated_date	= models.DateTimeField(null=True)
#     expired	= models.BooleanField(default=False)

# class Brand(models.Model):
#     product_type = models.ForeignKey(CategoryProduct,on_delete=models.RESTRICT,verbose_name="product")
#     brand_name = models.CharField(max_length=200,verbose_name="Category Product Name(English)")
#     brand_name_am = models.CharField(max_length=200,verbose_name="Category Product Name(Amharic)")
#     created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='brand_created_by',null=True)
#     created_date	= models.DateTimeField(auto_now_add=True)
#     last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='brand_updated_by',null=True)
#     last_updated_date	= models.DateTimeField(null=True)
#     expired	= models.BooleanField(default=False)

class CompanyDropdownsMaster(models.Model):
    name = models.CharField(max_length=200)
    chk_type = models.CharField(choices=(
        ('','Select Lookup/dropdown Types'),
        ('Forms of Ownership','Forms of Ownership'),
        ('Working hours','Working hours'),
        ('Certifications','Certifications'),
        ('Management Tools','Management Tools'),
        ('Source of Energy','Source of Energy'),
        ('Areas of Major Challenges','Areas of Major Challenges'),
        ('Industry Status Checklists','Industry Status Checklists'),
        ('Laboratory Test Analysis','Laboratory Test Analysis'),
        ('Laboratory Equipment','Laboratory Equipment'),
    ),max_length=200,verbose_name="Check List Types")
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT,
                                    editable=False,related_name="created_by_user")
    lastupdated_date = models.DateTimeField(null=True)
    lastupdated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,
                                    related_name='updated_by')
    expired = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class RegionMaster(models.Model):
    name = models.CharField(max_length=255,verbose_name="Region Name in English")
    name_am = models.CharField(max_length=255,verbose_name="Region Name in Amharic")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)

class UomMaster(models.Model):
    name = models.CharField(max_length=20,verbose_name="Unit of Measurement Short Name in English")
    name_am = models.CharField(max_length=20,verbose_name="Unit of Measurement Short Name in Amharic")
    timestamp = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class ProjectDropDownsMaster(models.Model):
    name = models.CharField(max_length=200)
    dropdown_type = models.CharField(choices=(
        ('','Select Lookup/dropdown Types'),
        ('Project Classification','Project Classification'),
        ('Land Acquisition','Land Acquisition'),
        ('Technology','Technology'),
        ('Automation','Automation'),
        ('Mode Of Project','Mode Of Project'),
        ('Facility Design','Facility Design'),
    ),max_length=200,verbose_name="Check List Types")
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT,
                                    editable=False,related_name="pl_creted_by")
    lastupdated_date = models.DateTimeField(null=True)
    lastupdated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,
                                    related_name='pl_updated_by')
    expired = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    

    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ('name',)

#pharmaceutical product group
class PharmaceuticalProduct(models.Model):
    name = models.CharField(max_length=255,verbose_name="Product Group Name")
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT,
                                    editable=False,related_name="pp_creted_by")
    lastupdated_date = models.DateTimeField(null=True)
    lastupdated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,
                                    related_name='pp_updated_by')
    expired = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)

class TherapeuticGroup(models.Model):
    name = models.CharField(max_length=255,verbose_name="Therapeutic Group")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT,
                                    editable=False,related_name="tg_creted_by")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)

class UserTracker(models.Model):
    ipaddress = models.GenericIPAddressField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class UserActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    model_name = models.CharField(max_length=200,null=True,blank=True)
    object_id = models.IntegerField(null=True,blank=True)
    before_change = models.CharField(max_length=255,null=True)
    after_change = models.CharField(max_length=255,null=True)
    activity = models.CharField(max_length=255,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
