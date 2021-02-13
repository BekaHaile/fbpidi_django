from rest_framework.views import APIView
from rest_framework import status, generics, authentication, permissions
from rest_framework.decorators import permission_classes, authentication_classes 
from rest_framework.response import Response

from company.models import Company
from company.api.serializers import CompanyInfoSerializer, CompanyFullSerializer

from product.models import Product, ProductImage, ProductPrice
from product.api.serializer import ProducteFullSerializer, ProductInfoSerializer, ProductImageSerializer

class ApiIndexView(APIView):
    pass

#product-by-category/  request.data['category_id']
class ApiProductByCategoryView(APIView):
     def get(self, request):
         products = Product.objects.filter(category = request.data['category_id'])
         return Response(
             data ={'count': products.count(),
                 'products': ProductInfoSerializer(products, many = True).data
               },
            status = status.HTTP_200_OK
         )


class ApiProductDetailView(APIView):
    def get(self, request):
        return Response( 
            data = ProducteFullSerializer( Product.objects.get(id = request.data['id']) ).data,
            status = status.HTTP_200_OK)

    
class ApiProfileView(APIView):
    pass

#product-by-main-category/ request.data['category']
class ApiProductByMainCategory(APIView):
    def get(self, request):
        category= request.data['category']
        products = []
        if category == "all":
            products=Product.objects.all()
        else:
            products = Product.objects.filter(category__category_name__category_type = category)
        return Response( data = { 'count':len(products), 
                                'products': ProductInfoSerializer(products, many = True).data},
                                 status = status.HTTP_200_OK
                        )

#client/comp-by-main-category/
class ApiCompanyByMainCategoryList(APIView):   
    #  request.data['company_type'] should be = manufacturer or supplier, request[product_category = "Beverage", "Food", "Pharmaceuticals", "all"]
    def get(self,request): 
        product_category = request.data['product_category']
        companies = Company.objects.filter(company_type= request.data['company_type']) #all companies with 
        if product_category != "all": # if it is "Beverage" or "Food" or "Pharmaceuticals"
            companies = companies.filter(product_category__category_name__category_type = product_category)
        return Response(
            data = {'count' : companies.count(), 'companies': CompanyInfoSerializer(companies, many =True).data},
            status= status.HTTP_200_OK)


class ApiCompanyDetailView(APIView):
    def get(self, request):
        return Response(
        data= CompanyFullSerializer( Company.objects.get(id = request.data['id']) ).data,
        status= status.HTTP_200_OK
        )


