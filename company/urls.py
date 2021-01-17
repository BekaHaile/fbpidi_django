from django.urls import path


from company.views import (
    CompaniesDetailView,CompaniesView,CreateCompanyProfile,CreateCompanyEvent,
    CreateCompanyProfileAfterSignUp,ViewCompanyProfile,CreateCompanySolution,CreateFbpidiCompanyProfile
)

# urlpatterns = [
#     path("create_company_profile/",CreateCompanyProfile.as_view(),name="create_company_profile"),
#     path("company_list/<option>/",CompaniesView.as_view(),name="companies"),
#     path("company_detail/<id>/",CompaniesDetailView.as_view(),name="company_detail"),
#     path("create_company_profile_al/",CreateCompanyProfileAfterSignUp.as_view() ,name='complete_company_profile'),
#     path("view_company_profile/",ViewCompanyProfile.as_view() ,name='view_company_profile'),
#     path("edit_company_profile/<id>/",ViewCompanyProfile.as_view(),name="edit_company_profile"),
#     path("create_company_solution/<company_id>",CreateCompanySolution.as_view(),name="create_company_solution"),
#     path("create_company_event/<company_id>",CreateCompanyEvent.as_view(),name="create_company_event"),
#     path("create_fbpidi_company/",CreateFbpidiCompanyProfile.as_view(),name="create_fbpidi_company"),
# ]