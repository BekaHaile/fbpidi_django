from django.urls import path


from company.views import (
    CompaniesDetailView,CompaniesView,CreateCompanyProfile,
    CreateCompanyProfileAfterSignUp,ViewCompanyProfile
)

urlpatterns = [
    path("create_company_profile/",CreateCompanyProfile.as_view(),name="create_company_profile"),
    path("company_list/<option>/",CompaniesView.as_view(),name="companies"),
    path("company_detail/<id>/",CompaniesDetailView.as_view(),name="company_detail"),
    path("create_company_profile_al/",CreateCompanyProfileAfterSignUp.as_view() ,name='complete_company_profile'),

]