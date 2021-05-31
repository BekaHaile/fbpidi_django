import random
import string
from django.core import paginator

from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpRequest, Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, generics, authentication, permissions
from rest_framework.decorators import permission_classes, authentication_classes, api_view 

from admin_site.models import Category
from admin_site.api.serializers import CategorySerializer, SubCategorySerializer

from collaborations.api.api_views import get_paginated_data, get_paginator_info

from company.models import Company
from company.api.serializers import CompanyInfoSerializer
from product.models import SubCategory,Product, ProductImage, ProductPrice,ProductLike
from product.api.serializer import (ProductFullSerializer, ProductInfoSerializer, ProductImageSerializer, ProductInquiryCreationSerializer)




def filter_products_by_name(products_list, name):
    return products_list.filter( Q(name__icontains= name) | Q(brand__brand_name__icontains = name) | Q(brand__product_type__sub_category_name__icontains=name)).distinct()


def user_liked_products(user):
    if user.is_authenticated:
        likes = ProductLike.objects.filter(user = user)
        return [l.product.id for l in likes]
    return []

class ApiUserLikedProducts(APIView):
    def get(self, request):
        try:
            return Response(data = {'error':False, 'liked_products':user_liked_products(request.user)})
        except Exception as e:
            return Response(data = {'error':True, 'message':str(e)})
            

class ApiProductByCategory(APIView):
     def get(self, request):
        try:
            category = Category.objects.get(id=request.query_params['category_id'])
            categories = Category.objects.filter(category_type = category.category_type).distinct()


            products = Product.objects.filter(brand__product_type__category_name__id = request.query_params['category_id'])
            if 'by_title' in request.query_params:
                products = filter_products_by_name( products, request.query_params['by_title'])
            
            products = get_paginated_data(request, products) #paginating the final result  
            return Response( data ={'error':False, 'paginator':get_paginator_info(products), 'liked_products':user_liked_products(request.user),
                                    'products': ProductInfoSerializer(products, many = True).data, 'categories': CategorySerializer( categories, many= True).data, },)
        except Exception as e:
            return Response( data = {'error':True, 'message': f'{str(e)}'})

# this is for listing products by main category(Food, Bevera, pharma or All ) and if from that page a search by_title is requested
# to list products by Category object use the ApiProductByCategory. It also can filter by name
class ApiProductByMainCategory(APIView):
    def get(self, request):
        try:
            products = Product.objects.all()
            categories = Category.objects.all().distinct()

            if 'category' in request.query_params and request.query_params['category'] != 'All': # if All, products without filtering 
                # category is  one of 'Food', "Beverage", "Pharmaceuticals":
                if request.query_params['category'] == "Pharmaceuticals":
                    products = products.filter(pharmacy_product_type__category_name__category_type = request.query_params['category'])
                else:
                    products = products.filter(brand__product_type__category_name__category_type = request.query_params['category'])
                categories = categories.filter(category_type = request.query_params['category'] )
            if 'by_title' in request.query_params:
                products = filter_products_by_name(products, request.query_params['by_title'])
            if 'by_company' in request.query_params:
                companies = Company.objects.filter( Q(name__in = request.query_params['by_company'].split(',')[:-1] )| Q(name_am__in =request.query_params['by_company'].split(',')[:-1]) )
                products = products.filter(company__in = companies)
            
            count = len(products)
            products=get_paginated_data(request, products)
            paginator = get_paginator_info(products)
            
            products = ProductInfoSerializer(products, many = True).data
            # if request.query_params['category'] == "Pharmaceuticals":
            #     for p in products:
            #         p['brand']={'id':0,  'product_type':p['pharmacy_product_type'],'brand_name':"None", "brand_name_am":"None"}
                    
            
            return Response( data = {'error': False, 'paginator': paginator, 'count':count, 'liked_products':user_liked_products(request.user),
                                    'products':products, 'categories':CategorySerializer(categories, many= True).data })
    
        except Exception as e:
            return Response(data ={'error':True, 'message':f"{str(e)}"})

        
class ApiProductDetailView(APIView):
    def get(self, request):
        try:
            product = get_object_or_404(Product, id = request.query_params['id'])
            return Response( data = {'error':False, 'product':ProductFullSerializer(product ).data, 'liked_products':user_liked_products(request.user)},)
        except Http404:
            return Response(data = {'error': True, 'message':'Product Not Found!'})


# this function is used to convert the list of string ids to integer and to cut the last , off
def get_id_list(str_id):
    prods_id_list = str_id[:-1] 
    product_ids = prods_id_list.split(",")
    return [int(i) for i in product_ids]
    

class ApiInquiryRequest(APIView):
    def get(self, request):
        try:
            selected_prods = Product.objects.filter(id__in = get_id_list( request.query_params['products']) )
            return Response({'error':False, 'products':ProductInfoSerializer(selected_prods, many=True).data, 'count':selected_prods.count()})
        except Exception as e:
            print("@@@@@@ Exception at InquiryForm get ",e)
            return Response({'error':True, 'message':str(e)})
    def post(self, request):
        try:
            products = Product.objects.filter(id__in = get_id_list( request.data['prod_id_list']) ).distinct()
            serializer = ProductInquiryCreationSerializer(data = request.data)

            if serializer.is_valid():
                for p in products:       
                    item = serializer.create(validated_data=request.data)
                    item.product = p
                    item.user=request.user
                    if 'attachement' in request.data:
                        item.attachement = request.data['attachement']
                    item.save()
                return Response(data={'error':False, 'email':request.data['sender_email']})
            else:
                print("form invalid")
                return Response(data={'error':True, 'message':serializer.errors})
            
        except Exception as e:
            print("@@@ Exception ",e)
            return Response(data= {'error':True, 'message':str(e)})
    
    
class ApiInquiryByCategory(APIView):
    def get(self, request):
        try:    
            category = Category.objects.get(id = request.query_params['category'])
            companies = Company.objects.filter(category =   category)
            company_ids = [c.id for c in companies ]
            return Response(data={'error':False, 'company_ids':company_ids,'count':len(company_ids),'category':request.query_params['category']})
    
        except Exception as e:
            print("@@@@@@ Exception at InquiryByCategory get ",e)
            return Response(data = {'error':True, 'message':str(e)})
    
    def post(self, request):
        try:
            category = Category.objects.get(id = request.data['category'])
            companies = category.company_category.all()
            serializer = ProductInquiryCreationSerializer(data = request.data)
            if serializer.is_valid():
                for c in companies:      
                    item = serializer.create(validated_data=request.data)
                    item.category = category
                    item.user=self.request.user
                    if 'attachement' in request.data:
                        item.attachement = request.data['attachement']
                    item.save()
                return Response(data={'error':False, 'email':request.data['sender_email']})
            else:
                print("invalid data")
                return Response(data = {'error':True, 'message':str(serializer.errors)})

        except Exception as e:
            print("@@@ Exception ",e)
            return Response(data = {'error':True, 'message':str(e)})


class ApiLikeProduct(APIView):
    def get(self, request):
        try:  
            product  = Product.objects.get (id= int(request.query_params['p_id'] ) )
            if ProductLike.objects.filter(user = request.user, product = product).exists():
                return Response(data = {'error':True, 'message': 'Already Liked product'})
            p_like = ProductLike( user = request.user, product = product  )
            p_like.save()
            return Response(data = {'error':False})

        except Exception as e:
            print("########Exception while tring to like a product ",e)
            return Response(data = {'error':True, 'message':str(e)})


class ApiDislikeProduct(APIView):
    def get(self, request):
        try:
            p_like = ProductLike.objects.filter(user = request.user, product = Product.objects.get (id= int(request.query_params['p_id'] ))).first()
            if p_like:
                p_like.delete()
            return Response({'error':False})
        except Exception as e:
            print("########Exception at Dislike product ",e)
            return Response({'error':True, 'message':str(e)})

        


       