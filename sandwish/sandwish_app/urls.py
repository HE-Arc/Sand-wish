from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),

    path("profile/<str:slug>/", views.ProfileView.as_view(), name="profile"),
    path("profile/<str:username>/<str:slug>/", views.WishlistView.as_view(), name="wishlist"),
]
