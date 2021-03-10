from rest_framework import serializers
from admin_site.api.serializers import CategorySerializer, SubCategorySerializer
from company.models import Company
from accounts.api.serializers import CompanyAdminSerializer
# from product.api.serializer import ProductInfoSerializer

class CompanyFullSerializer(serializers.ModelSerializer):
    product_category_name = serializers.CharField(source='get_product_category_type')
    user = CompanyAdminSerializer(read_only=True)
    class Meta:
        model = Company
        fields = ('__all__')

# serialize only light weight info, don't send haivy like company intro. 
# used for serializing multiple companies, like listing
class CompanyInfoSerializer(serializers.ModelSerializer):
    product_category_name = serializers.CharField(source='get_product_category_type')
    class Meta:
        model = Company
        fields = ('id','user','company_name','company_name_am','location','email','phone_number',
                    'detail','detail_am','company_logo','company_type','company_type_am','number_of_employees',
                    'established_year','certification','city','postal_code','product_category_name','product_category','color',
                    'facebook_link','twiter_link','google_link',)


class CompanyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id','user','company_name','company_name_am','location','email','phone_number',
                    'detail','detail_am','company_logo','company_type','company_type_am','number_of_employees',
                    'established_year','certification','city','postal_code','color',
                    'facebook_link','twiter_link','google_link',)


        
