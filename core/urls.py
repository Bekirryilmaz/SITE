from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hizmetlerimiz/', views.services, name='services'),
    path('hakkimizda/', views.about, name='about'),
    path('galeri/', views.gallery, name='gallery'),
    path('iletisim/', views.contact, name='contact'),
    path('tasinma-rehberi/', views.guide, name='guide'),
]
