from rest_framework import serializers
from admin_site.models import Category
from company.models import SubCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category()
        fields = '__all__'
class SubCategorySerializer(serializers.ModelSerializer):
        category_name = CategorySerializer
        class Meta:
            model = SubCategory()
            fields = '__all__'

