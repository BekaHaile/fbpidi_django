from django.urls import path,include

from .views import (PollIndex, PollDetail, VacancyMoreDetail,CreateComment,
                    CustomerTenderList, CustomerTenderDetail, CreateApplication, VacancyList, CategoryBasedSearch )

urlpatterns = [
    path("polls/", PollIndex.as_view(), name = "polls" ),
    path("poll_detail/<id>/", PollDetail.as_view(), name = "poll_detail"),

    path("tender_list/", CustomerTenderList.as_view(), name = "tender_list"),
    path("customer_tender_detail/<id>/", CustomerTenderDetail.as_view(), name = "customer_tender_detail"),
    # path("download_document/<id>/", DownloadDocument.as_view(), name = "download_document"),
    path("apply/<model_name>/<id>",CreateApplication.as_view(),name="applications"),
    path("vacancy-list/",VacancyList.as_view(),name="vacancy"),
    path("blog-comment/<id>",CreateComment.as_view(),name="Comment"),
    path("vacancy-search/<id>",CategoryBasedSearch.as_view(),name="vacancy_search"),
    path("vacancy-detail/<id>",VacancyMoreDetail.as_view(),name="vacancy_detail"),

    
        
]
