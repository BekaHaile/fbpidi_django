from django.urls import path, include
from core.api.api_views import (ApiIndexView, ApiCompanyByMainCategoryList, ApiCompanyDetailView,
                                ApiProductByMainCategory, ApiProductByCategoryView, ApiProductDetailView,
                                ApiProfileView)

from product.api.api_views import ApiCartSummary, ApiAddToCartView, ApiDecrementFromCart, ApiCheckout
from django.core.exceptions import ObjectDoesNotExist



urlpatterns = [

    path("home/", ApiIndexView.as_view(), name = "api_home"),
    path("accounts/", include("accounts.api.api_urls"), name = "api_account" ),# api login, logout ...
    path("collaborations/", include("collaborations.api.api_urls"), name = "api_collaborations"),
    
    
    #product related urls
    path("product-detail/", ApiProductDetailView.as_view(),name="api_product_detail"),
    path("product-by-category/",ApiProductByCategoryView.as_view(),name="api_product_category"),
    path("product-by-main-category/",ApiProductByMainCategory.as_view(),name="api_product_category_main"),
    
    #Company related urls    
    path("comp-by-main-category/",ApiCompanyByMainCategoryList.as_view(),name="api_company_category_main"),
    # path("sup_comp-by-main-category/<option>/",SupCompanyByMainCategory.as_view(),name="suplier_category_main"),
    path("company-detail/", ApiCompanyDetailView.as_view(), name = "api_company_detail"),
    
    #cart related urls
    path("add-to-cart/",ApiAddToCartView.as_view(),name="api_add_to_cart"),
    path("cart_summary/",ApiCartSummary.as_view(),name="api_cart_summary"),
    path("decrement_cart/",ApiDecrementFromCart.as_view(),name="api_decrement_cart"),
    path("checkout/",ApiCheckout.as_view(),name="api_checkout"),
    path("mydash/",ApiProfileView.as_view(),name="api_mydash"),
    # path("", include("accounts.urls")),




]