from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include('sandwish_app.urls')),
    
    #Add Django site authentication urls (for login, logout, password management)
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #Add media url
