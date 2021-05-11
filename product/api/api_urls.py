
from django.urls import path, include
from product.api.api_views import *

urlpatterns = [
    path("product-detail/", ApiProductDetailView.as_view(),name="api_product_detail"),
    path("product-by-category/",ApiProductByCategory.as_view(),name="api_product_category"),
    path("product-by-main-category/",ApiProductByMainCategory.as_view(),name="api_product_category_main"),
    path('product_inquiry/',ApiInquiryRequest.as_view(), name="api_product_inquiry"),
    path('inquiry_by_category/',ApiInquiryByCategory.as_view(), name ="api_category_inquiry"),
    path('like_product/', ApiLikeProduct.as_view(), name="api_like_product"),
    path('dislike_product/', ApiDislikeProduct.as_view(), name = "api_dislike_product"),

 

]