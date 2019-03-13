from django.urls import path, re_path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login_redirect/", views.login_redirect, name="login_redirect"),
    path("admin/", admin.site.urls),
    path("<slug:slug>/", views.ProfileView.as_view(), name="profile"),
    path("<slug:username>/wishlist/<pk>", views.WishlistView.as_view(), name="wishlist"),
    path("wishlist/delete/<pk>", views.WishlistDeleteView.as_view(), name="wishlist-delete"),
    path("gift/delete/<pk>", views.GiftDeleteView.as_view(), name="gift-delete"),
    path("gift/validate/<pk>", views.GiftValidateView.as_view(), name="gift-validate"),
    path("<slug:username>/wishlist/<pk>/create", views.GiftCreateView.as_view(), name="gift-create"),

]
