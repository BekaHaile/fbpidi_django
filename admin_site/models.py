
from django.db import models
from django.conf import settings
from django.utils import timezone

CAT_LIST = (
    ('','Select Main Category'),
    ("Food",'Food'),
    ("Beverage",'Beverages'),
    ("Pharmaceuticals",'Pharmaceuticals'),
)
class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=False,null=False)
    category_type = models.CharField(choices=CAT_LIST,max_length=200,verbose_name="Category Type(English)")
    category_type_am = models.CharField(choices=CAT_LIST,max_length=200,verbose_name="Category Type(Amharic)")
    category_name = models.CharField(max_length=200,verbose_name="Category Name(English)")
    category_name_am = models.CharField(max_length=200,verbose_name="Category Name(Amharic)")
    description = models.TextField(verbose_name="Description(English)")
    description_am = models.TextField(verbose_name="Description(Amharic)")
    image = models.ImageField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=False,null=False)
    category_name = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True,verbose_name="Category Type")
    sub_category_name = models.CharField(max_length=200,verbose_name="Sub-Category Name(English)")
    sub_category_name_am = models.CharField(max_length=200,verbose_name="Sub-Category Name(Amharic)")
    description = models.TextField(verbose_name="Description (English)")
    description_am = models.TextField(verbose_name="Description (Amharic)")
    image = models.ImageField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sub_category_name

class ChecklistMaster(models.Model):
    name = models.CharField(max_length=200)
    chk_type = models.CharField(choices=(
        ('','Select Check List Types'),
        ('Forms of Ownership','Forms of Ownership'),
        ('Working hours','Working hours'),
        ('Certifications','Certifications'),
        ('Managment Tools','Managment Tools'),
        ('Source of Energy','Source of Energy'),
        ('Support Types Needed from the Institute','Support Types Needed from the Institute'),
        ('Company Status Checklists','Company Status Checklists'),
    ),max_length=200,verbose_name="Check List Types")
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT,
                                    editable=False,related_name="created_by_user")
    lastupdated_date = models.DateTimeField(null=True)
    lastupdated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,
                                    related_name='updated_by')
    expired = models.BooleanField(default=False)

 