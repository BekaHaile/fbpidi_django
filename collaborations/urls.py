from django.urls import path,include
from .views import (PollIndex, PollDetail, 
                    CustomerTenderList, CustomerTenderDetail,  )

urlpatterns = [
    path("polls/", PollIndex.as_view(), name = "polls" ),
    path("poll_detail/<id>/", PollDetail.as_view(), name = "poll_detail"),

    path("tender_list/", CustomerTenderList.as_view(), name = "tender_list"),
    path("customer_tender_detail/<id>/", CustomerTenderDetail.as_view(), name = "customer_tender_detail"),
    # path("download_document/<id>/", DownloadDocument.as_view(), name = "download_document"),
    
        
]
