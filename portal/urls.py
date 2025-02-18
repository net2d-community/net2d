from django.urls import path
from portal import views

app_name = 'portal'
urlpatterns = [
    path('install/', views.index, name='index'),
    path('install/success', views.success, name='install-success'),
]
