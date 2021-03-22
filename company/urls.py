from django.urls import path
from company.views import (
    CompaniesDetailView,CompaniesView,CreateCompanyProfile,
    CreateFbpidiCompanyProfile, CompanyByMainCategory,
    ProjectList,ProjectDetail
)
from company.company_views import (CompanyHomePage, CompanyAbout, CompanyContact,CompanyProductList,
                                    CompanyProjectList, CompanyNewsList,CompanyNewsDetail,CompanyEventList,CompanyEventDetail,
                                    CompanyAnnouncementList, CompanyAnnouncementDetail, CompanyResearchList,CompanyTenderList,CompanyVacancyList,CompanyBlogList,
                                    CompanyPollList, CompanyTenderDetail,CompanyVacancyDetail, CompanyVacancyApply,CompanyBlogDetail, CompanyPollDetail,


)


urlpatterns = [
    path("man_comp-by-main-category/<option>/",CompanyByMainCategory.as_view(),name="manufac_category_main"),
    path("company-home-page/<pk>/",CompanyHomePage.as_view(),name="company_home"),
    path("about/<pk>/",CompanyAbout.as_view(),name="company_about"),
    path("contact/<pk>/",CompanyContact.as_view(),name="company_contact"),
    path("company-products/<pk>/",CompanyProductList.as_view(),name="company_products"),
    path("company-projects/<pk>/",CompanyProjectList.as_view(),name="company_projects"),

    path("company_research/<pk>/",CompanyProductList.as_view(),name="company_research"),
    path("company_announcement/<pk>/",CompanyAnnouncementList.as_view(),name="company_announcement"),
    # path("company_announcement_detail/<pk>/<company_pk>/",CompanyAnnouncementDetail.as_view(), name = "company_announcemnet_detail"),

    path("company_event/<pk>/",CompanyEventList.as_view(),name="company_event"),
    path("company_event/<pk>/<company_pk>/",CompanyEventDetail.as_view(),name="company_event_detail"),
    
    path("company_news/<pk>/",CompanyNewsList.as_view(),name="company_news"),
    path("company_news_detail/<pk>/<company_pk>/",CompanyNewsDetail.as_view(),name="company_news_detail"),
    
    path("company_tender/<pk>/",CompanyTenderList.as_view(),name="company_tender"),
    path("company_tender_detail/<pk>/<company_pk>/",CompanyTenderDetail.as_view(),name="company_tender_detail"),
    
    path("company_vacancy/<pk>/",CompanyVacancyList.as_view(),name="company_vacancy"),
    path("company_vacancy_detail/<pk>/<company_pk>/",CompanyVacancyDetail.as_view(),name="company_vacancy_detail"),
    path("company_vacancy_apply/<vacancy_pk>/", CompanyVacancyApply.as_view(), name = 'company_vacancy_apply'),
    
    path("company_blog/<pk>/",CompanyBlogList.as_view(),name="company_blog"),
    path("company_blog_detail/<pk>/<company_pk>/",CompanyBlogDetail.as_view(),name="company_blog_detail"),
    
    path("company_poll/<pk>/",CompanyPollList.as_view(),name="company_poll"),
    path("company_poll_detail/<id>/",CompanyPollDetail.as_view(),name="company_poll_detail"),
    
    path("company_faq/<pk>/",CompanyProductList.as_view(),name="company_faq"),
    path("project_list/",ProjectList.as_view(),name="project_list"),
    path("project_detail/<pk>/",ProjectDetail.as_view(),name="project_detail"),
]


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