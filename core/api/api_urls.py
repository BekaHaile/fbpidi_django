from django.urls import path, include
from core.api.api_views import (ApiIndexView, ApiCompanyByMainCategoryList, ApiCompanyDetailView,
                                ApiProductByMainCategory, ApiProductByCategoryView, ApiProductDetailView)



urlpatterns = [

    path("home/", ApiIndexView.as_view(), name = "client_home"),
    path("accounts/", include("accounts.api.api_urls"), name = "client_account" ),# api login, logout ...
    path("collaborations/", include("collaborations.api.api_urls"), name = "client_collaborations"),
    
    path("",ApiIndexView.as_view(),name='index'),

    #product related urls
    path("product-detail/", ApiProductDetailView.as_view(),name="product_detail"),
    path("product-by-category/",ApiProductByCategoryView.as_view(),name="product_category"),
    path("product-by-main-category/",ApiProductByMainCategory.as_view(),name="client_product_category_main"),
    
    #Company related urls    
    path("comp-by-main-category/",ApiCompanyByMainCategoryList.as_view(),name="client_company_category_main"),
    # path("sup_comp-by-main-category/<option>/",SupCompanyByMainCategory.as_view(),name="suplier_category_main"),
    path("company-detail/", ApiCompanyDetailView.as_view(), name = "client_company_detail"),
    # path("add-to-cart/<id>/",AddToCartView.as_view(),name="add_to_cart"),
    # path("cart_summary/",CartSummary.as_view(),name="cart_summary"),
    # path("decrement_cart/<id>/",DecrementFromCart.as_view(),name="decrement_cart"),
    # path("checkout/",CheckoutView.as_view(),name="checkout"),
    # path("mydash/",ProfileView.as_view(),name="mydash"),
    # path("", include("accounts.urls")),




]