from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from dhcpctrl import views

urlpatterns = [
    path('config/get/', views.config_get, name='config-get'),
    path('reservation/', views.reservation, name='reservation'),
]

urlpatterns = format_suffix_patterns(urlpatterns)