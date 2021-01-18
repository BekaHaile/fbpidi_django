from django.urls import path,include
from .views import PollIndex, PollDetail, CreateApplication, VacancyList, CategoryBasedSearch

urlpatterns = [
    path("polls/", PollIndex.as_view(), name = "polls" ),
    path("poll_detail/<id>/", PollDetail.as_view(), name = "poll_detail"),
    path("apply/<model_name>/<id>",CreateApplication.as_view(),name="applications"),
    path("vacancy-list/",VacancyList.as_view(),name="vacancy"),
    path("vacancy-search/<id>",CategoryBasedSearch.as_view(),name="vacancy_search"),

    
]