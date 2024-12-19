from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-roadmap/', views.get_roadmap, name='get-roadmap'),
]