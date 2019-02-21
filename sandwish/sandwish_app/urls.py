from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    re_path(r"^(?P<slug>[\w.@+-]+)/$", views.ProfileView.as_view(), name="profile"),
]
