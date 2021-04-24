from rest_framework import serializers
from company.models import Company, CompanyAddress, Certificates,  InvestmentProject
from accounts.api.serializers import CompanyAdminSerializer, UserInfoSerializer
from product.models import Category, SubCategory, Brand

# these serializers are in admin_site because if we put them in product.api.serializer there will be circular import with company serializers 
from admin_site.api.serializers import CategorySerializer, SubCategorySerializer, BrandSerializer



class CompanyAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAddress
        fields = ("__all__")


class CompanyCertificatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificates
        fields = ("__all__")


class CompanyFullSerializer(serializers.ModelSerializer):
    # product_category_name = serializers.CharField(source='get_product_category_type')

    contact_person = UserInfoSerializer(read_only=True)
    company_address = CompanyAddressSerializer(source = 'get_company_address', read_only=True)
    class Meta:
        model = Company
        fields = ('__all__')


# serialize only light weight info, don't send haivy like company intro. 
# used for serializing multiple companies, like listing
class CompanyInfoSerializer(serializers.ModelSerializer):
    # product_category_name = serializers.CharField(source='get_product_category_type')
    contact_person = UserInfoSerializer(read_only=True)
    company_address = CompanyAddressSerializer(source = 'get_company_address', many =False, read_only=True)
    company_certificates = CompanyCertificatesSerializer(source = 'get_company_certificates', many = True, read_only=True)
    category = CategorySerializer(source= 'get_company_category' , many =True, read_only = True) #b/c it is a manytomanyrelation
    
    class Meta:
        model = Company
        fields = ('id','contact_person','name','name_am','logo','detail','detail_am','geo_location','category', 'certification','established_yr', 'company_address','company_certificates')


class CompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id','name','name_am','logo')
        
class InvestmentProjectserializer(serializers.ModelSerializer):
    company =  CompanyInfoSerializer(read_only = True)
    contact_person = UserInfoSerializer(read_only=True)
    product_type = CategorySerializer(read_only = True, many =True)
    class Meta:
        model = InvestmentProject
        fields = "__all__"
