from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include('sandwish_app.urls')),

    #Add Django site authentication urls (for login, logout, password management)
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #Add media url
