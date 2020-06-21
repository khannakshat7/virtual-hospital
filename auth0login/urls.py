from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard', views.dashboard),
    path('logout', views.logoutp),
    path('appointment', views.appointmentpatient),
    path('done', views.done),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
]
