from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('face_verification/<uuid:uid>', views.verify_face, name="face_verify"),
    path('', views.verify_acccount, name="verifyaccount"),
    path('s', views.Success, name="success"),
    path('f', views.Failed, name="fail"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

