from django.contrib import admin
from functools import update_wrapper
from django.template.response import TemplateResponse
from django.urls import path
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
# from accounts.forms import UserCreationForm
# views from accounts app
from accounts.views import (CompanyAdminSignUpView,UserListView,RolesView,UserLogView,
                        UserDetailView,UpdateAdminProfile,CreateUserView,GroupView,
                        create_company_after_signup_view,CreateCompanyProfileView)
# views from admin_site app
from admin_site.views import (AdminIndex,CategoryView,CreateCategories,CategoryDetail,
                        CompaniesView,CompaniesDetailView,DeleteView,
                        AdminProductListView,CreateProductView,ProductDetailView,
                        AddProductImage,CreatePrice,
                        Polls, CreatePoll, AddChoice, EditPoll,EditChoice, DeletePoll, DetailPoll, DeleteChoice)


class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            wrapper.admin_site = self
            return update_wrapper(wrapper, view)

        my_urls = [
            path('', wrap(AdminIndex.as_view()),name="admin_home"),
            path("signup/",CompanyAdminSignUpView.as_view(),name="signup"),
            path("create_user/",wrap(CreateUserView.as_view()),name="create_user"),
            path("users_list/",wrap(UserListView.as_view()),name="users_list"),
            path("roles_list/",wrap(RolesView.as_view()),name="roles_list"),
            path("user_detail/<option>/<id>/",wrap(UserDetailView.as_view()),name="user_detail"),
            path("update_profile/",wrap(UpdateAdminProfile.as_view()),name="add_profile"),
            path("user_audit/",wrap(UserLogView.as_view()),name="useraudit"),
            path("manage_group/",wrap(GroupView.as_view()),name="group_view"),

            path("categories/<option>/",wrap(CategoryView.as_view()),name="p_categories"),
            path("create_category/<option>",wrap(CreateCategories.as_view()),name="create_category"),
            path("category_edit/<option>/<cat_id>/",wrap(CategoryDetail.as_view()),name="edit_category"),
            path("comp_profile/<option>/<id>/",wrap(CreateCompanyProfileView.as_view()),name="comp_profile"),
            path("company_list/<option>/",wrap(CompaniesView.as_view()),name="companies"),
            path("company_detail/<id>/",wrap(CompaniesDetailView.as_view()),name="company_detail"),
            path("delete/<model_name>/<id>/",wrap(DeleteView.as_view()),name="delete"),
            path("products_list/<user_type>/",wrap(AdminProductListView.as_view()),name="admin_products"),
            path("create_product/",wrap(CreateProductView.as_view()),name="create_product"),
            path("product_detail/<option>/<id>/",wrap(ProductDetailView.as_view()),name="product_detail"),
            path("add_more_images/",wrap(AddProductImage.as_view()),name="add_product_image"),
            path("create_price/",wrap(CreatePrice.as_view()),name="create_price"),
            path("create_company_profile_al/<id>/",wrap(create_company_after_signup_view),name='complete_company_profile'),
        
            # paths for polls app, 
            path("polls/", wrap(Polls.as_view()), name = "admin_polls"),
            path("create_poll/", wrap(CreatePoll.as_view()), name = "create_poll"),
            path("edit_poll/<id>/", wrap(EditPoll.as_view()), name = "edit_poll"),
            path("add_choice/<id>/", wrap(AddChoice.as_view()), name = "add_choice"),
            path("edit_choice/", wrap(EditChoice.as_view()), name = "edit_choice"), #choice id is found from adit_poll.html option tag
            path("delete_poll/<id>/", wrap(DeletePoll.as_view()), name = "delete_poll"),
            path("delete_choice/<id>/", wrap(DeleteChoice.as_view()), name = "delete_choice"),
            path("detail_poll/<id>/", wrap(DetailPoll.as_view()), name = "detail_poll"),

        
        ]
        return my_urls + urls


admin_site = CustomAdminSite(name='myadmin')