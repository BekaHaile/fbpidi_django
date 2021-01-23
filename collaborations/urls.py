from django.urls import path,include
from .views import (PollIndex, PollDetail, 
                    CustomerTenderList, CustomerTenderDetail, CreateApplication, VacancyList, CategoryBasedSearch, ApplyForTender,  pdf_download )

urlpatterns = [
    path("polls/", PollIndex.as_view(), name = "polls" ),
    path("poll_detail/<id>/", PollDetail.as_view(), name = "poll_detail"),

    path("tender_list/", CustomerTenderList.as_view(), name = "tender_list"),
    path("customer_tender_detail/<id>/", CustomerTenderDetail.as_view(), name = "customer_tender_detail"),
    path("tender_application/<id>/", ApplyForTender.as_view(), name= "tender_application"),
    path("download/<id>/", pdf_download, name = "download"),

    path("vacancy-list/",VacancyList.as_view(),name="vacancy"),
    path("vacancy-search/<id>",CategoryBasedSearch.as_view(),name="vacancy_search"),

    
        
]
