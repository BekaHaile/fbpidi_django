from rest_framework import serializers
from admin_site.api.serializers import CategorySerializer, SubCategorySerializer
from company.models import Company, CompanyAddress, Certificates,  InvestmentProject
from product.models import Brand, SubCategory
from accounts.api.serializers import CompanyAdminSerializer, UserInfoSerializer
from admin_site.models import Category
from admin_site.api.serializers import CategorySerializer, SubCategorySerializer
# from product.api.serializer import ProductInfoSerializer
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

    created_by = CompanyAdminSerializer(read_only=True)
    company_address = CompanyAddressSerializer(source = 'get_company_address', read_only=True)
    class Meta:
        model = Company
        fields = ('__all__')


# serialize only light weight info, don't send haivy like company intro. 
# used for serializing multiple companies, like listing
class CompanyInfoSerializer(serializers.ModelSerializer):
    # product_category_name = serializers.CharField(source='get_product_category_type')
    created_by = CompanyAdminSerializer(read_only=True)
    company_address = CompanyAddressSerializer(source = 'get_company_address', many =False, read_only=True)
    company_certificates = CompanyCertificatesSerializer(source = 'get_company_certificates', many = True, read_only=True)
    category = CategorySerializer(source= 'get_company_category' , many =True, read_only = True) #b/c it is a manytomanyrelation
    
    class Meta:
        model = Company
        fields = ('id','created_by','name','name_am','logo','geo_location','category', 'certification','established_yr', 'company_address','company_certificates')


class InvestmentProjectserializer(serializers.ModelSerializer):
    company =  CompanyInfoSerializer(read_only = True)
    contact_person = UserInfoSerializer(read_only=True)
    product_type = CategorySerializer(read_only = True, many =True)
    class Meta:
        model = InvestmentProject
        fields = "__all__"


    

    
    # location =
    # phone_number =
    # email =
    # city_town =
    # 'facebook_link','twiter_link','google_link',
    # 'company_type',
    # 'company_type_am',
    # 'number_of_employees',
    # 'postal_code',
    # 'product_category_name',
    # 'product_category','color',


class BrandSerializer(serializers.ModelSerializer):
    product_type = SubCategorySerializer
    class Meta:
        model = Brand
        fields = ( 'product_type', 'brand_name','brand_name_am')


