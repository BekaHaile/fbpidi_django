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
    price = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
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

class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    to_company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} of {}".format(self.quantity,self.product.name)
    
    def get_total_item_price(self):
        return self.product.price * self.quantity

    def get_total_discount_item_price(self):
        if self.product.discount:
            return self.product.discount * self.quantity
    
    def get_saving_price(self):
        if self.product.discount:
            return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.product.discount:
            return self.get_total_discount_item_price()
        else:
            return self.get_total_item_price()

    def get_max_quantity(self):
        return int(self.quantity)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct,related_name='products',default="")
    ref_code = models.CharField(max_length=30)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    # shipping_address = models.ForeignKey('ShippingAddress',
    #                             on_delete=models.SET_NULL, 
    #                             blank=True, null=True)
    # payement = models.ForeignKey('Payement',
    #                             on_delete=models.SET_NULL, 
    #                             blank=True, null=True)
    # coupon = models.ForeignKey("Coupon",on_delete=models.SET_NULL, 
    #                             blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    time_stamp = models.DateTimeField(auto_now_add=True)


    def get_total_price(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

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
    

