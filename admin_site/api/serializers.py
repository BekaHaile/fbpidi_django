from rest_framework import serializers
from admin_site.models import Category
from product.models import SubCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_type', 'category_type_am', 'category_name','category_name_am', 'description', 'description_am', 'icons')
        
class SubCategorySerializer(serializers.ModelSerializer):
        category_name = CategorySerializer(read_only = True)
        class Meta:
            model = SubCategory()
            fields = ('compay','category_name','sub_category_name','sub_category_name_am',
                    'description', 'description_am', 'icons')
                    

