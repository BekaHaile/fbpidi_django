from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import get_object_or_404

from django.http import HttpResponse, HttpRequest, Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, authentication, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes, api_view 


from admin_site.models import Category,SubCategory
from admin_site.api.serializers import CategorySerializer, SubCategorySerializer

from collaborations.models import News
from collaborations.api.serializers import NewsListSerializer

from company.models import Company
from company.api.serializers import CompanyInfoSerializer, CompanyFullSerializer

from product.models import Product, ProductImage, ProductPrice, Order, OrderProduct, InvoiceRecord
from product.api.serializer import (ProducteFullSerializer, ProductInfoSerializer, ProductImageSerializer,
                                     OrderSerializer, OrderProductSerializer, ShippingAddressSerializer)
        
from product.forms import CheckoutForm

from django.utils import timezone
import random
import string

class ApiCartSummary(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def response(self, request, message = ""):
        try:
                order = Order.objects.get(user=request.user,ordered=False)
                products = Product.objects.all().order_by("timestamp")[:4]
                count = 0
                for product_order in order.products.all():
                    count += product_order.quantity

                return { 'data' : {'message': message,'total_orders':count,'orders':OrderSerializer( order).data, 
                                    'products': ProductInfoSerializer( products, many = True).data
                                        }, 
                         'error':False,
                        'status': status.HTTP_200_OK
                }
        except ObjectDoesNotExist:
                return{'error':True, 'message':"You Do Not have active order"}

    def get(self, request):
        return Response( self.response( request ))
     

class ApiAddToCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.data['id']:
            try:
                product = get_object_or_404(Product,id=int(request.data['id']))
            except Exception:
                return Response({'error':True, 'message': "Product not Found!"})

            order_product,created = OrderProduct.objects.get_or_create(
                product=product,
                to_company=product.company,
                user=self.request.user,
                ordered=False
            )
            user_order_queryset = Order.objects.filter(
                user=self.request.user,
                ordered=False
            )
            if user_order_queryset.exists():
                order = user_order_queryset[0]
                if order.products.filter(product__id=product.id).exists():
                    order_product.quantity +=1
                    order_product.save()
                    #12345 redirect to cart summary
                    return Response( ApiCartSummary.response(self, request, f"You order additional {product.name}" ))
                else:
                    order.products.add(order_product)
                    order.save()
                    return Response( ApiCartSummary.response(self, request,"New Product is added to your cart" ))
            else:
                order = Order.objects.create(user=self.request.user,order_date=timezone.now())
                order.products.add(order_product)
                order.save()
                return Response( ApiCartSummary.response(self, request,"The Order is added to your cart"  ))

        else:
            return Response({'error':True, 'message':"No Input with keyword 'id'!!"})


class ApiDecrementFromCart(APIView):
    authentication_classes = ([TokenAuthentication])
    permission_classes = ([IsAuthenticated])
    
    def get(self,request):
        if request.data['id']:
            try:
                product = get_object_or_404(Product,id=int(request.data['id']))
            except Exception:
                return Response({'error':True, 'message': "Product not Found!"})
            product = get_object_or_404(Product,id=request.data['id'])
            user_order_queryset = Order.objects.filter(user=request.user,ordered=False)
            if user_order_queryset.exists():
                order = user_order_queryset[0]
                if order.products.filter(product__id=product.id).exists():
                    order_product = OrderProduct.objects.filter( 
                        user=self.request.user,product=product,ordered=False )[0]
                    if order_product.quantity > 1:
                        order_product.quantity -= 1
                        order_product.save()
                        return Response( ApiCartSummary.response(self, request, f"You removed 1 {order_product.product.name} from your cart." ))
                        
                    else:
                        order.products.remove(order_product)
                        return Response( ApiCartSummary.response(self, request, f"You removed all {order_product.product.name}s from your cart." ))
                else:   
                    return Response({'error':True, 'message':"This item was not in your cart"})
            else: 
                return Response({'error':True, 'message': "You do not have order"})   
        
        else:
            return Response({'error':True, 'message':"No Input with keyword 'id'!!"})


def create_ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits,k=30))

def create_invoice(invoice,user):
    return '#INV-'.join(random.choices(string.ascii_uppercase + (str(invoice.id).join(str(user.id)))))

class ApiCheckout(APIView):
    authentication_classes = ([TokenAuthentication])
    permission_classes = ([IsAuthenticated])
    def get(self, request):
        order = Order.objects.get(user=request.user,ordered=False)
        return Response( data = {'error':False,
                                 'order': OrderSerializer(order).data},
                        status = status.HTTP_200_OK
                        )
    
    def post(self, request):
        
        if ShippingAddressSerializer(data = request.data).is_valid(raise_exception=True):
            serializer = ShippingAddressSerializer(data = request.data)
            shipping = serializer.create(validated_data = request.data, user = request.user)
        try:
            order = Order.objects.get(user=request.user,ordered=False)
        except Exception:
            return Response({'error':True, 'message': "Order object not Found!"})

        
        order.shipping_address = shipping
        invoice = InvoiceRecord(
            user=request.user,
            amount=order.get_total_price()
            
        )
        #12345 join create_invoice(invoice,request.user)
        invoice.code = create_invoice(invoice,request.user)
        invoice.save()
        order.invoice = invoice
        order.ordered = True
        order.save()
        return Response(data = {'error':False,'invoice_code':order.invoice.code, 'message':"Successfull"})





        


       