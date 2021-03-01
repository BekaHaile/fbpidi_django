from django.urls import path, include
from company.api.api_views import ApiCompanyByMainCategoryList, ApiCompanyDetailView


urlpatterns = [
    #Company related urls    
    path("comp-by-main-category/",ApiCompanyByMainCategoryList.as_view(),name="api_company_category_main"),
    # path("sup_comp-by-main-category/<option>/",SupCompanyByMainCategory.as_view(),name="suplier_category_main"),
    path("company-detail/", ApiCompanyDetailView.as_view(), name = "api_company_detail"),
]