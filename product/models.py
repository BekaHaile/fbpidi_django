from django.db import models
from django.conf import settings
from django.utils import timezone

from admin_site.models import Category
from company.models import Company

UOM=(
    ('Pieces', 'Pieces'),
    ('Bags', 'Bags'),
    ('Boxes', "Boxes")
)
# This is For Product/Type
class SubCategory(models.Model):
    category_name = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,
									blank=True,verbose_name="Category Type",related_name="sub_category")
    sub_category_name = models.CharField(max_length=200,verbose_name="Product Name(English)")
    sub_category_name_am = models.CharField(max_length=200,verbose_name="Product Name(Amharic)")
    uom = models.CharField(max_length=25,verbose_name="Unit of Measurement")
    description = models.TextField(verbose_name="Description (English)")
    description_am = models.TextField(verbose_name="Description (Amharic)")
    icons = models.ImageField( verbose_name="Product Icon")
    created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='product_created_by',null=True)
    created_date	= models.DateTimeField(auto_now_add=True)
    last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='product_updated_by',null=True)
    last_updated_date	= models.DateTimeField(null=True)
    expired	= models.BooleanField(default=False)

    def __str__(self):
        return self.sub_category_name
# Brand
class Brand(models.Model):
	company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="company_brand")
	product_type = models.ForeignKey(SubCategory,on_delete=models.CASCADE, verbose_name="Product Type", related_name="product_category")
	brand_name = models.CharField(max_length=200,verbose_name="Product Brand Name(English)")
	brand_name_am = models.CharField(max_length=200,verbose_name="Product Brand Name(Amharic)")
	created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='brand_created_by',null=True)
	created_date	= models.DateTimeField(auto_now_add=True)
	last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='brand_updated_by',null=True)
	last_updated_date	= models.DateTimeField(null=True)
	expired	= models.BooleanField(default=False)

	def __str__(self):
		return self.brand_name	
# This is the specific Product or Varayti
class Product(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="company_product")
    name = models.CharField(max_length=255,verbose_name="Varayti Name(English)")
    name_am = models.CharField(max_length=255,verbose_name="Varayti Name(Amharic)")
    # fandb_category = models.ForeignKey(SubCategory,on_delete=models.CASCADE, blank=True,null=True,
    #                              verbose_name="Product Category",related_name="product_fandb_category")
    # pharmacy_category = models.ForeignKey(Category,on_delete=models.CASCADE, blank=True,null=True, 
    #                                     verbose_name="Pharmacy Product Category",related_name="pharmacy_category")
    brand = models.ForeignKey(Brand,on_delete=models.RESTRICT,verbose_name="Varayti Brand",null=True,blank=True,related_name="varayti_brand")
    quantity = models.FloatField(verbose_name="Product Quantity",default=0)
    therapeutic_group = models.CharField(max_length=255,verbose_name="Therapeutic Group",null=True,blank=True)
    dose = models.ForeignKey('Dose',on_delete=models.RESTRICT,null=True,blank=True,related_name="product_dose")
    dosage_form = models.ForeignKey('DosageForm',on_delete=models.RESTRICT,null=True,blank=True,related_name="product_dosage_form")
    description = models.TextField(verbose_name="Varayti Description(English)")
    description_am = models.TextField(verbose_name="Varayti Description(Amharic)")
    image = models.ImageField()
    created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='varayti_created_by',null=True)
    created_date	= models.DateTimeField(auto_now_add=True)
    last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='varayti_updated_by',null=True)
    last_updated_date	= models.DateTimeField(null=True)
    expired	= models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def price(self):
        return ProductPrice.objects.filter(product=self).latest('created_date') if ProductPrice.objects.exists() else None
   
    def more_images(self):
        return ProductImage.objects.filter(product=self)

    def get_category(self):
        # is this like return self.company.category.category_name
        return [self.pharmacy_category.category_name, self.pharmacy_category.category_name_am]
        # return self.category.category_name.category_type
    
    class Meta:
        ordering = ('-created_date',)

class Dose(models.Model):
    dose = models.TextField(verbose_name="Dose in English")
    dose_am = models.TextField(verbose_name="Dose in Amharic")
    created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='dose_created_by',null=True)
    created_date	= models.DateTimeField(auto_now_add=True)
    last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='dose_updated_by',null=True)
    last_updated_date	= models.DateTimeField(null=True)
    expired	= models.BooleanField(default=False)

    def __str__(self):
        return self.dose
    
class DosageForm(models.Model):
    dosage_form = models.CharField(verbose_name="Dosage Form in English",max_length=255)
    dosage_form_am = models.CharField(verbose_name="Dosage Form in Amharic",max_length=255)
    description = models.TextField(verbose_name="Dosage Form Description in English")
    description_am = models.TextField(verbose_name="Dosage Form Description in Amharic")
    created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='dosage_created_by',null=True)
    created_date	= models.DateTimeField(auto_now_add=True)
    last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='dosage_updated_by',null=True)
    last_updated_date	= models.DateTimeField(null=True)
    expired	= models.BooleanField(default=False)

    def __str__(self):
        return self.dosage_form

class ProductionCapacity(models.Model):	 	
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="company_production_capacity")	
    product	= models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name="production_capacity") 
    p_date = models.DateField()
    install_prdn_capacity	= models.IntegerField(default=0,verbose_name="Installed Production Capacity")		
    atnbl_prdn_capacity = models.FloatField(default=0,verbose_name="Attainable Production Capacity")		
    actual_prdn_capacity = models.FloatField(default=0,verbose_name="Actual Production Capacity")		
    production_plan	= models.FloatField(default=0,verbose_name="Production Plan")		
    extraction_rate	= models.FloatField(default=0,verbose_name="Average Extraction Rate")	
    created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='prdn_created_by',null=True)
    created_date	= models.DateTimeField(auto_now_add=True)
    last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='prdn_updated_by',null=True)
    last_updated_date	= models.DateTimeField(null=True)
    expired	= models.BooleanField(default=False)

class ProductPackaging(models.Model):
    PACKAGING_CATEGORY =  (('','Select Packaging Category'),('Primary','Primary'),('Secondary','Secondary'),('Teritiary','Teritiary'))
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="company_product_packaging")
    product	= models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name="product_packaging")
    packaging	= models.CharField(verbose_name="Pckaging Type", max_length=2000)	 
    category	= models.CharField(verbose_name="Packaging Category", max_length=200, choices=PACKAGING_CATEGORY)
    amount = models.IntegerField(verbose_name="Amount",default=0)	 
    local_input	= models.FloatField(default=0,verbose_name="Source of Local Inputs in %")			
    import_input	= models.FloatField(default=0,verbose_name="Source of Imported Inputs in %")			
    wastage	= models.IntegerField(verbose_name="Wastage in %",default=0)	
    created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='package_created_by',null=True)
    created_date	= models.DateTimeField(auto_now_add=True)
    last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='package_updated_by',null=True)
    last_updated_date	= models.DateTimeField(null=True)
    expired	= models.BooleanField(default=False)		

class ProductionAndSalesPerformance(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="company_product_perfornamce")
    product	= models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name="sales_performance")
    activity_year	= models.IntegerField()			 
    production_amount	= models.FloatField(default=0,verbose_name="Total Production Amount")			
    sales_amount	= models.FloatField(default=0,verbose_name="Total Sales Amount")			
    sales_value	= models.FloatField(default=0,verbose_name="Total Sales Value in Birr")
    created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='performance_created_by',null=True)
    created_date	= models.DateTimeField(auto_now_add=True)
    last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='performance_updated_by',null=True)
    last_updated_date	= models.DateTimeField(null=True)
    expired	= models.BooleanField(default=False)

class AnnualInputNeed(models.Model):				
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="company_product_input")
    product	= models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name="input_need")
    input_name = models.CharField(max_length=255,verbose_name="Product Input")
    year = models.IntegerField()
    is_active_input	= models.BooleanField(default=False,verbose_name="Active or Not-Active Input")		
    amount	= models.FloatField(default=0,verbose_name="Amount")			
    local_input	= models.FloatField(default=0,verbose_name="Local Inputs in %")			
    import_input	= models.FloatField(default=0,verbose_name="Imported Imputs in %")
    created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='inputs_created_by',null=True)
    created_date	= models.DateTimeField(auto_now_add=True)
    last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='inputs_updated_by',null=True)
    last_updated_date	= models.DateTimeField(null=True)
    expired	= models.BooleanField(default=False)	

    def __str__(self):
        return self.input_name

class InputDemandSupply(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="company_product_demand")
    product	= models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name="product_input_demand_supply")
    input_type	= models.CharField(max_length=255,verbose_name="Input Type")
    year = models.IntegerField()		
    demand	= models.FloatField(default=0,verbose_name="Input Demand")			
    supply	= models.FloatField(default=0,verbose_name="Input Supply")
    created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='demand_created_by',null=True)
    created_date	= models.DateTimeField(auto_now_add=True)
    last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='demand_updated_by',null=True)
    last_updated_date	= models.DateTimeField(null=True)
    expired	= models.BooleanField(default=False)	



class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_image")
    product_image = models.ImageField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class ProductPrice(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_price")
    price = models.DecimalField(max_digits=10,decimal_places=2)
    startdate = models.DateField()
    end_date = models.DateField()
    created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='price_created_by',null=True)
    created_date	= models.DateTimeField(auto_now_add=True)
    last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='price_updated_by',null=True)
    last_updated_date	= models.DateTimeField(null=True)
    expired	= models.BooleanField(default=False)
    

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


class ProductInquiry(models.Model):
    sender_email = models.EmailField(verbose_name="sender email",)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    subject = models.CharField(max_length=200,)
    quantity = models.IntegerField()
    pieces = models.CharField(max_length=100)
    content = models.TextField()
    attachement = models.FileField(upload_to = "InquiryDocument/", max_length=254, verbose_name="Inquiry document",help_text="pdf, Max size 3MB", blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self):
        self.pieces = self.product.brand.product_type.uom
        super(ProductInquiry, self).save()


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
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="review")
    rating = models.IntegerField()
    review = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)


class AbuseReport(models.Model):
    url_link = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    message  = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    

