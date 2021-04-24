from rest_framework import serializers
from product.models import Category, SubCategory, Brand, Product, ProductImage, ProductPrice

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
    latest_price = ProductPriceSerializer(source='price', many = False)
    class Meta:
        model  = Product
        fields = ('id','name', 'name_am','latest_price', 'company', 'brand', 
                'therapeutic_group','dose','description','description_am', 'image', 'created_date')

