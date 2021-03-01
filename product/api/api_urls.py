
from django.urls import path, include
from product.api.api_views import ApiCartSummary, ApiAddToCartView, ApiDecrementFromCart, ApiCheckout, ApiProductDetailView, ApiProductByCategoryView, ApiProductByMainCategory

urlpatterns = [
    path("product-detail/", ApiProductDetailView.as_view(),name="api_product_detail"),
    path("product-by-category/",ApiProductByCategoryView.as_view(),name="api_product_category"),
    path("product-by-main-category/",ApiProductByMainCategory.as_view(),name="api_product_category_main"),
    path("add-to-cart/",ApiAddToCartView.as_view(),name="api_add_to_cart"),
    path("cart_summary/",ApiCartSummary.as_view(),name="api_cart_summary"),
    path("decrement_cart/",ApiDecrementFromCart.as_view(),name="api_decrement_cart"),
    path("checkout/",ApiCheckout.as_view(),name="api_checkout"),
]