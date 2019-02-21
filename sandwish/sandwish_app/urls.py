from django.urls import path, re_path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("admin/", admin.site.urls),
    path("<str:slug>/", views.ProfileView.as_view(), name="profile"),
]
