from django.urls import path, re_path
from django.contrib import admin

from . import views

urlpatterns = [
    # general
    #path("admin/", admin.site.urls), # commented for production
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login_redirect/", views.login_redirect, name="login_redirect"),

    # search
    path("search/", views.search, name="search"),
    path("search-redirect/", views.search_redirect, name="search_redirect"),
    path("search/<search>", views.index, name="index_search"),

    # user profile
    path("<slug:slug>/", views.ProfileView.as_view(), name="profile"),

    # wishlist
    path("<slug:username>/wishlist/<int:pk>", views.WishlistView.as_view(), name="wishlist"),
    path("<slug:username>/wishlist/<int:pk>/delete", views.WishlistDeleteView.as_view(), name="wishlist-delete"),

    #  gift
    path("<slug:username>/wishlist/<int:pk>/gift/create", views.GiftCreateView.as_view(), name="gift-create"),
    path("<slug:username>/wishlist/<int:w_pk>/gift/<int:pk>/delete", views.GiftDeleteView.as_view(), name="gift-delete"),
    path("<slug:username>/wishlist/<int:w_pk>/gift/<int:pk>/validate", views.GiftValidateView.as_view(), name="gift-validate"),

    # contribution
    path("contribution/create/", views.contribute, name="create-contribution"),
]
