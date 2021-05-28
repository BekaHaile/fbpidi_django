from django.urls import path, include
from core.api.api_views import (ApiIndexView,ApiProfileView,ApiTotalViewerData)


urlpatterns = [

    path("home/", ApiIndexView.as_view(), name = "api_home"),
    path("mydash/",ApiProfileView.as_view(),name="api_mydash"),
    path("total_viewers/",ApiTotalViewerData.as_view(), name="total_viewers"),
    
]