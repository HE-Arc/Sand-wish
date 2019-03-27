from django.urls import path, re_path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login_redirect/", views.login_redirect, name="login_redirect"),
    path("search/", views.search, name="search"),
    path("search-redirect/", views.search_redirect, name="search_redirect"),
    path("search/<search>", views.index, name="index_search"),
    path("admin/", admin.site.urls),
    path("<slug:slug>/", views.ProfileView.as_view(), name="profile"),
    path("<slug:username>/wishlist/<int:pk>", views.WishlistView.as_view(), name="wishlist"),
    path("wishlist/delete/<int:pk>", views.WishlistDeleteView.as_view(), name="wishlist-delete"),
    path("gift/delete/<int:pk>", views.GiftDeleteView.as_view(), name="gift-delete"),
    path("<slug:username>/wishlist/<int:pk>/create", views.GiftCreateView.as_view(), name="gift-create"),
    path("contribution/create/", views.create_contribution, name="create-contribution"),

]
