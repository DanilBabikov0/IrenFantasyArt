# artworks/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('artwork/<slug:slug>/', views.artwork_detail, name='artwork_detail'),
    path('collections/', views.collections_list, name='collections'),
    path('collection/<slug:slug>/', views.collection_detail, name='collection_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms, name='terms'),
    path('search/', views.search, name='search'),
]