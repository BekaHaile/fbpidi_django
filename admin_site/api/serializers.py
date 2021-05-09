from rest_framework import serializers
from admin_site.models import Category
from product.models import Category, SubCategory, Brand

# the order from product to Category is 
# product.brand.product_type.category_name for the models Product.Brand.SubCategory.Category
  

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','category_type', 'category_type_am', 'category_name','category_name_am', 'icons')
        
class SubCategorySerializer(serializers.ModelSerializer):
        category_name = CategorySerializer(read_only = True)
        class Meta:
            model = SubCategory
            fields = ('id','category_name','sub_category_name','sub_category_name_am','icons')


class BrandSerializer(serializers.ModelSerializer):
    product_type = SubCategorySerializer(read_only = True)
    class Meta:
        model = Brand
        fields = ( 'id','product_type', 'brand_name','brand_name_am')
