
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

# class OrderProduct(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     ordered = models.BooleanField(default=False)
#     time_stamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return "{} of {}".format(self.quantity,self.product.name)
    
#     def get_total_item_price(self):
#         return self.product.price * self.quantity

#     def get_total_discount_item_price(self):
#         if self.product.discount:
#             return self.product.discount * self.quantity
    
#     def get_saving_price(self):
#         if self.product.discount:
#             return self.get_total_item_price() - self.get_total_discount_item_price()

#     def get_final_price(self):
#         if self.product.discount:
#             return self.get_total_discount_item_price()
#         else:
#             return self.get_total_item_price()

#     def get_max_quantity(self):
#         return int(self.quantity)

# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#     products = models.ManyToManyField(OrderProduct,related_name='products',default="")
#     ref_code = models.CharField(max_length=30)
#     start_date = models.DateTimeField(auto_now_add=True)
#     order_date = models.DateTimeField()
#     ordered = models.BooleanField(default=False)
#     shipping_address = models.ForeignKey('ShippingAddress',
#                                 on_delete=models.SET_NULL, 
#                                 blank=True, null=True)
#     payement = models.ForeignKey('Payement',
#                                 on_delete=models.SET_NULL, 
#                                 blank=True, null=True)
#     coupon = models.ForeignKey("Coupon",on_delete=models.SET_NULL, 
#                                 blank=True, null=True)
#     being_delivered = models.BooleanField(default=False)
#     received = models.BooleanField(default=False)
#     refund_requested = models.BooleanField(default=False)
#     refund_granted = models.BooleanField(default=False)
#     time_stamp = models.DateTimeField(auto_now_add=True)


#     def get_total_price(self):
#         total = 0
#         for order_product in self.products.all():
#             total += order_product.get_final_price()
#         if self.coupon:
#             total -= self.coupon.amount
#         return total


# class ShippingAddress(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
#     company = models.CharField(max_length=200,default="")
#     street_address = models.CharField(max_length=100)
#     home_address = models.CharField(max_length=100)
#     town = models.CharField(max_length=50)
#     region = models.CharField(max_length=50)
#     zipcode = models.CharField(max_length=50)
#     phone_no = models.CharField(max_length=50)
#     delivery_note = models.TextField(null=True)
#     time_stamp = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.user.username 


# class Payement(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
#     charge_id = models.CharField(max_length=255)
#     amount = models.FloatField()
#     times_tamp = models.DateTimeField(auto_now_add=True)



# class Coupon(models.Model):
#     code = models.CharField(max_length=100)
#     amount = models.FloatField()
#     description = models.TextField()
#     time_stamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.code


