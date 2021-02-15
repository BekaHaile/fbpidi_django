from rest_framework import serializers
from admin_site.api.serializers import CategorySerializer, SubCategorySerializer
from company.api.serializers import CompanyInfoSerializer, CompanyFullSerializer
from product.models import Product, ProductImage, ProductPrice
from accounts.api.serializers import CompanyAdminSerializer

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProducteFullSerializer(serializers.ModelSerializer):
    category = SubCategorySerializer(read_only=True)
    company = CompanyFullSerializer(read_only=True)
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
    category_name = serializers.CharField(source='get_category')
    company = CompanyInfoSerializer
    class Meta:
        model  = Product
        fields = "__all__"

