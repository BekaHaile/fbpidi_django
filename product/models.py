from django.db import models
from django.conf import settings
from django.utils import timezone


from admin_site.models import SubCategory
from company.models import Company

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=False)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
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


class Review(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)


class AbuseReport(models.Model):
    url_link = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    message  = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    

