from rest_framework import serializers

from accounts.api.serializers import CompanyAdminSerializer, UserSerializer

from admin_site.api.serializers import CategorySerializer, SubCategorySerializer
from company.api.serializers import CompanyInfoSerializer, CompanyFullSerializer, BrandSerializer

from product.models import Product, ProductImage, ProductPrice, Order, OrderProduct, ShippingAddress, InvoiceRecord

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('product_image',)


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ('price', 'start_date','end_date')


class ProducteFullSerializer(serializers.ModelSerializer):
    company = CompanyInfoSerializer(read_only=True)
    fandb_category = BrandSerializer(read_only=True)
    pharmacy_category = CategorySerializer(read_only=True)
    more_images = serializers.SerializerMethodField('get_more_images')
    latest_price = ProductPriceSerializer(source='price', many = False)
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
    fandb_category = BrandSerializer(read_only = True)
    pharmacy_category = CategorySerializer
    latest_price = ProductPriceSerializer(source='price', many = False)
    class Meta:
        model  = Product
        fields = ('company','name', 'name_am', 'fandb_category', 'pharmacy_category', 'latest_price', 'uom', 'quantity',
                'therapeutic_group','dose','description','description_am', 'image')


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductInfoSerializer(read_only=True, required = False)
    class Meta:        
        model = OrderProduct
        fields = "__all__"


class ShippingAddressSerializer(serializers.ModelSerializer):
        user = UserSerializer( required=False)
        delivery_note = serializers.CharField(required=False, default="")

        class Meta:
            model = ShippingAddress
            fields = "__all__"

        def create(self, validated_data, user):
            shipping = ShippingAddress(user= user,  city=validated_data['city'],
                    first_name=validated_data['first_name'], last_name=validated_data['last_name'],
                    phone_no=validated_data['phone_no'], company=validated_data['company'],
                    street_address =validated_data['street_address'], home_address = validated_data['home_address'],
                    email=validated_data['email'])
            
            shipping.delivery_note = validated_data['delivery_note'] if validated_data['delivery_note'] else "" 
            shipping.save()
            return shipping
        

class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.FloatField(source='get_total_price')
    products = OrderProductSerializer(many = True, read_only=True, required=False)
    class Meta:
        model = Order
        fields = "__all__"
    

