from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include('sandwish_app.urls')),
    
    #Add Django site authentication urls (for login, logout, password management)
    path("accounts/", include("django.contrib.auth.urls")),
]
