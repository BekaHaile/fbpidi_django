from django.urls import path,include

from .views import (BlogList,BlogDetail,FaqList,
                    PollIndex, PollDetail, VacancyMoreDetail,CreateComment,
                    CustomerTenderList, CustomerTenderDetail, CreateApplication, VacancyList,
                    CategoryBasedSearch, CreateForumQuestion , ListForumQuestions,ForumQuestionsDetail,
                    CreateCommentReplay,ListAnnouncement,EditCommentForum,EditForumQuestions,
                    SearchForum, ApplyForTender,  pdf_download)
                    

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

    path("faq/",FaqList.as_view(),name="faq"),
    path("blog-list/",BlogList.as_view(),name="blog_grid_right"),
    path("blog-details/<id>",BlogDetail.as_view(),name="blog_details"),
    path("blog-comment/<id>",CreateComment.as_view(),name="Comment"),

    path("vacancy-list/",VacancyList.as_view(),name="vacancy"),
    path("vacancy-search/<id>",CategoryBasedSearch.as_view(),name="vacancy_search"),
    path("vacancy-detail/<id>",VacancyMoreDetail.as_view(),name="vacancy_detail"),

    
        
]
