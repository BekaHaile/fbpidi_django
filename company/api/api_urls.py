from django.urls import path, include
from company.api.api_views import (ApiCompanyByMainCategoryList, ApiSearchCompany, ApiCompanyDetailView, ApiProject,
         ApiProjectDetail, ApiLikeCompany, ApiDislikeCompany,ApiUserLikedCompanies, ApiCompanyUs, ApiContactCompany)


urlpatterns = [
    #Company related urls    
    path("comp-by-main-category/",ApiCompanyByMainCategoryList.as_view(),name="api_company_category_main"),
    path("search_company/", ApiSearchCompany.as_view(), name = "api_search_company"),
    # path("sup_comp-by-main-category/<option>/",SupCompanyByMainCategory.as_view(),name="suplier_category_main"),
    path("company-detail/", ApiCompanyDetailView.as_view(), name = "api_company_detail"),
    path('like_company/', ApiLikeCompany.as_view(), name = "api_like_company"),
    path('dislike_company/', ApiDislikeCompany.as_view(), name= "api_dislike_company"),
    path('user_liked_companies/', ApiUserLikedCompanies.as_view(), name = "user_liked_companies"),
    path('company_about_us/', ApiCompanyUs.as_view(), name = "api_about_us"),
    path('contact_company/', ApiContactCompany.as_view(), name = 'api_contact_company'),

    path("projects_list/", ApiProject.as_view(), name = "api_project_list"),
    path("project_detail/", ApiProjectDetail.as_view(), name = "api_project_detail"),
]