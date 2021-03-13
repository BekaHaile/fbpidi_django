from django.db import models
from django.conf import settings
from django.utils import timezone


from company.models import Company,SubCategory

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=False)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,verbose_name="Product Name(English)")
    name_am = models.CharField(max_length=255,verbose_name="Product Name(Amharic)")
    category = models.ForeignKey(SubCategory,on_delete=models.CASCADE, blank=True,null=True, verbose_name="Product Category")
    description = models.TextField(verbose_name="Product Description(English)")
    description_am = models.TextField(verbose_name="Product Description(Amharic)")
    discount = models.FloatField(default=0.0)
    image = models.ImageField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def price(self):
        return ProductPrice.objects.filter(product=self).latest('timestamp')
   
    
    def more_images(self):
        return ProductImage.objects.filter(product=self)

    def get_category(self):
        return self.category.category_name.category_type


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
        return str(self.price)


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
        return self.product.price().price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct,related_name='products',default="")
    ref_code = models.CharField(max_length=30)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('ShippingAddress',
                                on_delete=models.SET_NULL, 
                                blank=True, null=True)
    invoice = models.ForeignKey('InvoiceRecord',
                                on_delete=models.SET_NULL, 
                                blank=True, null=True)
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
            total += order_product.get_total_item_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    company = models.CharField(max_length=200,default="")
    city = models.CharField(max_length=200)
    street_address = models.CharField(max_length=100)
    home_address = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone_no = models.CharField(max_length=50)
    delivery_note = models.TextField(null=True)
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.city


class InvoiceRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    code = models.CharField(max_length=200)
    amount = models.FloatField()
    paid = models.BooleanField(default=False)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_code

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
    

