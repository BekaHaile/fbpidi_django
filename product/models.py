from django.db import models
from django.conf import settings
from django.utils import timezone

CAT_LIST = (
    ("Food",'Food'),
    ("Beverages",'Beverages'),
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
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=False,null=False)
    category_name = models.ForeignKey(Category,on_delete=models.CASCADE,null=False,blank=False,verbose_name="Category Type")
    sub_category_name = models.CharField(max_length=200,verbose_name="Sub-Category Name(English)")
    sub_category_name_am = models.CharField(max_length=200,verbose_name="Sub-Category Name(Amharic)")
    description = models.TextField(verbose_name="Description (English)")
    description_am = models.TextField(verbose_name="Description (Amharic)")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sub_category_name

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=False)
    name = models.CharField(max_length=255,verbose_name="Product Name(English)")
    name_am = models.CharField(max_length=255,verbose_name="Product Name(Amharic)")
    category = models.ForeignKey(SubCategory,on_delete=models.CASCADE, blank=True,null=True, verbose_name="Product Category")
    description = models.TextField(default="",verbose_name="Product Description(English)")
    description_am = models.TextField(default="",verbose_name="Product Description(Amharic)")
    image = models.ImageField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def username(self):
        return self.user.username

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

class ProductPrice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    startdate = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.price