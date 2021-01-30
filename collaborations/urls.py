from django.urls import path,include

from .views import (PollIndex, PollDetail, VacancyMoreDetail,CreateComment,
                    CustomerTenderList, CustomerTenderDetail, CreateApplication, VacancyList,
                    CategoryBasedSearch, CreateForumQuestion , ListForumQuestions,ForumQuestionsDetail,
                    CreateCommentReplay,ListAnnouncement,EditCommentForum,EditForumQuestions,
                    SearchForum, ApplyForTender,  pdf_download, 
                    CustomerNewsList, CustomerNewsDetail , CustomerEventList, CustomerEventDetail, EventParticipation)
                    

urlpatterns = [ 
    path("polls/", PollIndex.as_view(), name = "polls" ),
    path("poll_detail/<id>/", PollDetail.as_view(), name = "poll_detail"),
    path("edit-comment/<id>/<forum>/<type>/",EditCommentForum.as_view(),name="edit_comment"),
    path("forum-edit/<id>",EditForumQuestions.as_view(),name="forum_edit"),
    path("forum-search",SearchForum.as_view(),name="forum_search"),
    path("forum-form",CreateForumQuestion.as_view(),name="forum_form"),
    path("announcement-list/",ListAnnouncement.as_view(),name="announcement_list"),
    path("apply/<model_name>/<id>",CreateApplication.as_view(),name="applications"),
    path("forum-list",ListForumQuestions.as_view(),name="forum_list"),
    path("Replay-comment/<id>/<forum>",CreateCommentReplay.as_view(),name="Replay_comment"),
    path("forum-detail/<id>",ForumQuestionsDetail.as_view(),name="forum_detail"),
    path("tender_list/", CustomerTenderList.as_view(), name = "tender_list"),
    path("customer_tender_detail/<id>/", CustomerTenderDetail.as_view(), name = "customer_tender_detail"),
    path("tender_application/<id>/", ApplyForTender.as_view(), name= "tender_application"),
    path("download/<id>/", pdf_download, name = "download"),

    path("vacancy-list/",VacancyList.as_view(),name="vacancy"),
    path("blog-comment/<id>",CreateComment.as_view(),name="Comment"),
    path("vacancy-search/<id>",CategoryBasedSearch.as_view(),name="vacancy_search"),
    path("vacancy-detail/<id>",VacancyMoreDetail.as_view(),name="vacancy_detail"),

    ##News
    path("customer_news_list/", CustomerNewsList.as_view(), name = "customer_news_list"),
    path("customer_news_detail/<id>/", CustomerNewsDetail.as_view(), name = "customer_news_detail"),
    ##Events
    path("customer_event_list/", CustomerEventList.as_view(), name = "customer_event_list"),
    path("customer_event_detail/<id>/", CustomerEventDetail.as_view(), name = "customer_event_detail"),
    path("event_participation/<id>/", EventParticipation.as_view(), name="event_participation"),

    
        
]
