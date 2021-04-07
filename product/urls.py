from django.urls import path,include
from product.views.views import  (AddToCartView,CartSummary,DecrementFromCart,CheckoutView,SearchProduct,
 ProductDetailView, ProductByCategoryView, ProductByMainCategory,CreateReview, FetchInquiryProducts, InquiryRequest, LikeProduct)


urlpatterns = [
    path("product-detail/<pk>", ProductDetailView.as_view(),name="product_detail"),
    path("create-review/<product>", CreateReview.as_view(),name="create_review"),
    path("product-by-category/<cat_id>/",ProductByCategoryView.as_view(),name="product_category"),
    path("product-by-main-category/<option>/",ProductByMainCategory.as_view(),name="product_category_main"),
    path("search-products/",SearchProduct.as_view(),name='search_product'),
    path("add-to-cart/<id>/",AddToCartView.as_view(),name="add_to_cart"),
    path("cart_summary/",CartSummary.as_view(),name="cart_summary"),
    path("decrement_cart/<id>/",DecrementFromCart.as_view(),name="decrement_cart"),
    path("checkout/",CheckoutView.as_view(),name="checkout"),

    path("fetch_inquiry_products/", FetchInquiryProducts, name = "fetch_inquiry_products"),
    path("inquiry_form/", InquiryRequest.as_view(), name = "inquiry_form"),
    path('like_product/', LikeProduct, name = "like_product"),
    

    
]