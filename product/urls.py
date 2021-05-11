from django.urls import path,include
from product.views.views import  (SearchProduct,InquiryByCategory,
                                    ProductDetailView, ProductByCategoryView,
                                    ProductByProductView, ProductByMainCategory,
                                    CreateReview, FetchInquiryProducts,CategoriesView,
                                    InquiryRequest, LikeProduct)


urlpatterns = [
    path("product-detail/<pk>", ProductDetailView.as_view(),name="product_detail"),
    path("create-review/<product>", CreateReview.as_view(),name="create_review"),
    path("product-by-category/<cat_id>/",ProductByCategoryView.as_view(),name="product_category"),
    path("product-by-product/<cat_id>/",ProductByProductView.as_view(),name="product_product_category"),
    path("product-by-main-category/<option>/",ProductByMainCategory.as_view(),name="product_category_main"),
    path("search-products/",SearchProduct.as_view(),name='search_product'),

    path("fetch_inquiry_products/", FetchInquiryProducts, name = "fetch_inquiry_products"),
    path("inquiry_form/", InquiryRequest.as_view(), name = "inquiry_form"),
    
    path("category_inquiry_form/", InquiryByCategory.as_view(), name = "category_inquiry_form"),
    path('like_product/', LikeProduct, name = "like_product"),
    
    path("categories/<category>/",CategoriesView.as_view(),name="categories")
    
]