from rest_framework import serializers
from product.models import Category, SubCategory, Brand, Product, ProductImage, ProductPrice, ProductInquiry, ProductInquiryReply

from accounts.api.serializers import CompanyAdminSerializer, UserSerializer
from company.api.serializers import CompanyInfoSerializer, CompanyFullSerializer
# these serializers are in admin_site because if we put them in product.api.serializer there will be circular import with company serializers 
from admin_site.api.serializers import CategorySerializer, SubCategorySerializer, BrandSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('product_image',)


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ('price', 'start_date','end_date')


class ProductFullSerializer(serializers.ModelSerializer):
    company = CompanyInfoSerializer(read_only=True)
    brand = BrandSerializer(read_only = True)
    pharmacy_product_type = SubCategorySerializer(read_only = True)
    latest_price = ProductPriceSerializer(source='price', many = False)
    more_images = serializers.SerializerMethodField('get_more_images')
    
    class Meta:
        model = Product
        fields = "__all__"
    
    def get_more_images(self, product):
        image_urls = []
        for product_image in product.more_images():
            image_urls.append( product_image.image.url)
        return image_urls


class ProductInfoSerializer(serializers.ModelSerializer):
    company = CompanyInfoSerializer(read_only=True)
    brand = BrandSerializer(read_only = True)
    pharmacy_product_type = SubCategorySerializer(read_only = True)
    latest_price = ProductPriceSerializer(source='price', many = False)
    class Meta:
        model  = Product
        fields = ('id','name', 'name_am','latest_price', 'company', 'brand', 
                'therapeutic_group','dose','description','description_am', 'image', 'created_date')


# class JobApplicationCreationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = JobApplication
#         fields = ('status', 'bio','cv', 'documents','experiance','grade','institiute','field',) 
    
#     def create(self, validated_data):
#         vacancy = Vacancy.objects.get(id = validated_data['id'])
#         application = JobApplication(vacancy = vacancy, status =validated_data['status'],
#         bio=validated_data['bio'], cv=validated_data['cv'],documents=validated_data['documents'],experiance=validated_data['experiance'],
#         grade=validated_data['grade'],field=validated_data['field'], institiute=validated_data['institiute'])
#         return application
        
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="user_inquiry")
    # product = models.ForeignKey(Product, on_delete = models.CASCADE, blank = True, null = True)
    # category = models.ForeignKey(Category, on_delete = models.CASCADE, blank = True, null = True)
    # attachement = models.FileField(upload_to = "InquiryDocument/", max_length=254, verbose_name="Inquiry document",help_text="pdf, Max size 3MB", blank=True)
    
class ProductInquiryCreationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductInquiry
        fields = ('sender_email','subject','quantity','content')
    
    def create(self, validated_data):
        inquiry = ProductInquiry(sender_email=validated_data['sender_email'], subject=validated_data['subject'], content=validated_data['content'], quantity=validated_data['quantity'])
        return inquiry

class ProductInquirySerializer(serializers.ModelSerializer):
    product = ProductInfoSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    reply = serializers.SerializerMethodField('get_reply')
    class Meta:
        model = ProductInquiry
        fields = "__all__"

    def get_reply(self, inquiry):
        inquiry_reply = inquiry.productinquiryreply_set.first()
        if inquiry_reply:
            return {'reply':inquiry_reply.reply, 'created_date':inquiry_reply.created_date}
        else:
            return None