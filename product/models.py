from django.db import models
from django.conf import settings
from django.utils import timezone

from admin_site.models import Category,UomMaster,TherapeuticGroup,PharmaceuticalProduct
from company.models import Company

UOM=(
    ('Pieces', 'Pieces'),
    ('Bags', 'Bags'),
    ('Boxes', "Boxes")
)
# This is For Product/Type
class SubCategory(models.Model):
    category_name = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,
									blank=True,verbose_name="Sub Sector",related_name="sub_category")
    sub_category_name = models.CharField(max_length=200,verbose_name="Product Name(English)")
    sub_category_name_am = models.CharField(max_length=200,verbose_name="Product Name(Amharic)")
    uom = models.ForeignKey(UomMaster,on_delete=models.RESTRICT,default=1,related_name='product_unit',verbose_name="Unit of Measurement")
    description = models.TextField(verbose_name="Description (English)",default="")
    description_am = models.TextField(verbose_name="Description (Amharic)",default="")
    icons = models.ImageField( verbose_name="Product Icon")
    created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='product_created_by',null=True)
    created_date	= models.DateTimeField(auto_now_add=True)
    last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='product_updated_by',null=True)
    last_updated_date	= models.DateTimeField(null=True)
    expired	= models.BooleanField(default=False)

    def __str__(self):
        return self.sub_category_name

    class Meta:
        ordering = ('sub_category_name',)
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
    brand = models.ForeignKey(Brand,on_delete=models.RESTRICT,verbose_name="Varayti Brand",null=True,blank=True,related_name="varayti_brand")
    
    pharmacy_product_type = models.ForeignKey(SubCategory,on_delete=models.CASCADE, blank=True,null=True, verbose_name="Pharmacy Product Category",related_name="pharmacy_category")
    
    quantity = models.FloatField(verbose_name="Product Quantity",default=0)
    therapeutic_group = models.ForeignKey(TherapeuticGroup,on_delete=models.RESTRICT,related_name="therapeutic_group",verbose_name="Therapeutic Group",null=True,blank=True)
    dose = models.CharField(max_length=255,verbose_name="Dose & Packaging",null=True,blank=True)
    dosage_form = models.ForeignKey('DosageForm',on_delete=models.RESTRICT,null=True,blank=True,related_name="product_dosage_form")
    description = models.TextField(verbose_name="Varayti Description(English)")
    description_am = models.TextField(verbose_name="Varayti Description(Amharic)")
    image = models.ImageField()
    is_active = models.BooleanField(default=False)
    reserve_attr0 = models.ForeignKey(PharmaceuticalProduct,on_delete=models.RESTRICT,related_name='product_group',null=True,blank=True,
                            verbose_name="Pharmaceutical Product Group")
    reserve_attr1 = models.CharField(max_length=255,default="")
    reserve_attr2 = models.CharField(max_length=255,default="")
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

    def count_likes(self):
        return self.productlike_set.all().count()

    # this returns the Category object for a product using the order => product.brand.subcategory.category
    def get_category(self):
        
        if self.company.main_category == 'Pharmaceuticals':
            return self.pharmacy_product_type.category_name
        else:
            return self.brand.product_type.category_name

    def get_subcategory(self):
        try:
            if self.company.main_category == 'Pharmaceuticals':
                return self.pharmacy_product_type
                
            else:
                return self.brand.product_type
        except Exception as e:
            return ''
                # return self.brand.product_type.sub_category_name
            
             

    def rating(self):
        total = 0
        reviews =self.product_review.all()
        for r in reviews:
            total += r.rating
        try:
            return total/reviews.count()
        except Exception:
            return 0
    
    class Meta:
        ordering = ('-created_date',)

class ProductLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    created_date = models.DateField(auto_now_add=True)


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

    class Meta:
        ordering = ('dose',)
        
class DosageForm(models.Model):
    dosage_form = models.CharField(verbose_name="Dosage Form in English",max_length=255)
    dosage_form_am = models.CharField(verbose_name="Dosage Form in Amharic",max_length=255)
    created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='dosage_created_by',null=True)
    created_date	= models.DateTimeField(auto_now_add=True)
    last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='dosage_updated_by',null=True)
    last_updated_date	= models.DateTimeField(null=True)
    expired	= models.BooleanField(default=False)

    def __str__(self):
        return self.dosage_form
    
    class Meta:
        ordering = ('dosage_form',)

class ProductionCapacity(models.Model):	 	
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="company_production_capacity")	
    product	= models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name="production_capacity") 
    year = models.IntegerField(default=0)
    install_prdn_capacity	= models.FloatField(default=0,verbose_name="Installed Production Capacity")		
    atnbl_prdn_capacity = models.FloatField(default=0,verbose_name="Attainable Production Capacity")		
    actual_prdn_capacity = models.FloatField(default=0,verbose_name="Actual Production Capacity")		
    production_plan	= models.FloatField(default=0,verbose_name="Production Plan")		
    extraction_rate	= models.FloatField(default=0,verbose_name="Average Extraction Rate")
    is_active = models.BooleanField(default=False)
    reserve_attr0 = models.CharField(max_length=255,default="")
    reserve_attr1 = models.CharField(max_length=255,default="")
    reserve_attr2 = models.CharField(max_length=255,default="")	
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
    input_unit = models.ForeignKey(UomMaster,on_delete=models.RESTRICT,blank=True, null=True,verbose_name="Unit Of Measurement")
    category	= models.CharField(verbose_name="Packaging Category", max_length=200, choices=PACKAGING_CATEGORY)
    amount = models.FloatField(verbose_name="Amount",default=0)	 
    local_input	= models.FloatField(default=0,verbose_name="Source of Local Inputs in %")			
    import_input	= models.FloatField(default=0,verbose_name="Source of Imported Inputs in %")			
    wastage	= models.IntegerField(verbose_name="Wastage in %",default=0)
    is_active = models.BooleanField(default=False)
    reserve_attr0 = models.CharField(max_length=255,default="")
    reserve_attr1 = models.CharField(max_length=255,default="")
    reserve_attr2 = models.CharField(max_length=255,default="")	
    created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='package_created_by',null=True)
    created_date	= models.DateTimeField(auto_now_add=True)
    last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='package_updated_by',null=True)
    last_updated_date	= models.DateTimeField(null=True)
    expired	= models.BooleanField(default=False)		

class ProductionAndSalesPerformance(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="company_product_perfornamce")
    product	= models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name="sales_performance")
    activity_year	= models.IntegerField(verbose_name="Production & Sales Performance Year")	
    half_year = models.CharField(max_length=100,verbose_name="Half Year Data")		 
    production_amount	= models.FloatField(default=0,verbose_name="Total Production Amount")			
    sales_amount	= models.FloatField(default=0,verbose_name="Total Sales Amount")			
    sales_value	= models.FloatField(default=0,verbose_name="Total Sales Value in Birr")
    is_active = models.BooleanField(default=False)
    reserve_attr0 = models.CharField(max_length=255,default="")
    reserve_attr1 = models.CharField(max_length=255,default="")
    reserve_attr2 = models.CharField(max_length=255,default="")
    created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='performance_created_by',null=True)
    created_date	= models.DateTimeField(auto_now_add=True)
    last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='performance_updated_by',null=True)
    last_updated_date	= models.DateTimeField(null=True)
    expired	= models.BooleanField(default=False)

class AnnualInputNeed(models.Model):				
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="company_product_input")
    product	= models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name="input_need")
    input_name = models.CharField(max_length=255,verbose_name="Product Input")
    input_unit = models.ForeignKey(UomMaster,on_delete=models.RESTRICT,null=True,verbose_name="Unit Of Measurement")
    year = models.IntegerField()
    is_active_input	= models.BooleanField(default=False,verbose_name="Active or Not-Active Input")		
    amount	= models.FloatField(default=0,verbose_name="Amount")			
    local_input	= models.FloatField(default=0,verbose_name="Local Inputs in %")			
    import_input	= models.FloatField(default=0,verbose_name="Imported Imputs in %")
    is_active = models.BooleanField(default=False)
    reserve_attr0 = models.CharField(max_length=255,default="")
    reserve_attr1 = models.CharField(max_length=255,default="")
    reserve_attr2 = models.CharField(max_length=255,default="")
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
    input_unit = models.ForeignKey(UomMaster,on_delete=models.RESTRICT,null=True,verbose_name="Unit Of Measurement")
    year = models.IntegerField(verbose_name="Demand & Supply Year")	
    half_year = models.CharField(max_length=100,verbose_name="Half Year Data")
    demand	= models.FloatField(default=0,verbose_name="Input Demand")			
    supply	= models.FloatField(default=0,verbose_name="Input Supply")
    is_active = models.BooleanField(default=False)
    reserve_attr0 = models.CharField(max_length=255,default="")
    reserve_attr1 = models.CharField(max_length=255,default="")
    reserve_attr2 = models.CharField(max_length=255,default="")
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


class ProductInquiry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="user_inquiry")
    sender_email = models.EmailField(verbose_name="sender email",)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, blank = True, null = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, blank = True, null = True)
    subject = models.CharField(max_length=200,)
    quantity = models.IntegerField()
    pieces = models.CharField(max_length=100)
    content = models.TextField()
    replied = models.BooleanField(default=False)
    attachement = models.FileField(upload_to = "InquiryDocument/", max_length=254, verbose_name="Inquiry document",help_text="pdf, Max size 3MB", blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']


    def save(self):
        if self.product :
            self.pieces = self.product.brand.product_type.uom.name
            super(ProductInquiry, self).save()
        else:
            super(ProductInquiry, self).save()          

class ProductInquiryReply(models.Model):
    inquiry = models.ForeignKey(ProductInquiry, on_delete = models.CASCADE)
    reply = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']


class Review(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_review")
    rating = models.IntegerField(default=2)
    review = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)

