from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('request-dump/', views.request_dump, name='request-dump'),
    path('sw-deploy/', views.sw_deploy, name='sw-deploy'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
