from django.urls import path,include
from product.views import  AddToCartView,CartSummary,DecrementFromCart,CheckoutView, ProductDetailView, ProductByCategoryView, ProductByMainCategory


urlpatterns = [
    path("product-detail/<id>", ProductDetailView.as_view(),name="product_detail"),
    path("product-by-category/<cat_id>/",ProductByCategoryView.as_view(),name="product_category"),
    path("product-by-main-category/<option>/",ProductByMainCategory.as_view(),name="product_category_main"),
    path("add-to-cart/<id>/",AddToCartView.as_view(),name="add_to_cart"),
    path("cart_summary/",CartSummary.as_view(),name="cart_summary"),
    path("decrement_cart/<id>/",DecrementFromCart.as_view(),name="decrement_cart"),
    path("checkout/",CheckoutView.as_view(),name="checkout"),
    
]