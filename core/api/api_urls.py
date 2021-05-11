from django.urls import path, include
from core.api.api_views import (ApiIndexView,ApiProfileView,ApiTotalViewerData)

from django.core.exceptions import ObjectDoesNotExist
from admin_site.models import Category



urlpatterns = [

    path("home/", ApiIndexView.as_view(), name = "api_home"),
    path("mydash/",ApiProfileView.as_view(),name="api_mydash"),
    path("total_viewers/",ApiTotalViewerData.as_view(), name="total_viewers"),
    #product related urls
    # path("product-detail/", ApiProductDetailView.as_view(),name="api_product_detail"),
    # path("product-by-category/",ApiProductByCategory.as_view(),name="api_product_category"),
    # path("product-by-main-category/",ApiProductByMainCategory.as_view(),name="api_product_category_main"),
    
    # #Company related urls    
    # path("comp-by-main-category/",ApiCompanyByMainCategoryList.as_view(),name="api_company_category_main"),
    # # path("sup_comp-by-main-category/<option>/",SupCompanyByMainCategory.as_view(),name="suplier_category_main"),
    # path("company-detail/", ApiCompanyDetailView.as_view(), name = "api_company_detail"),
    
    #cart related urls
    # path("add-to-cart/",ApiAddToCartView.as_view(),name="api_add_to_cart"),
    # path("cart_summary/",ApiCartSummary.as_view(),name="api_cart_summary"),
    # path("decrement_cart/",ApiDecrementFromCart.as_view(),name="api_decrement_cart"),
    # path("checkout/",ApiCheckout.as_view(),name="api_checkout"),

    #user profile
    
    # path("", include("accounts.urls")),




]