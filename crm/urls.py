from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('supervision', views.supervision, name='crm_supervision'),
    path('leads/', views.leads, name='crm_leads'),
    path('leads/edit/<uuid:pk>/', views.lead_edit, name='lead_edit'),
    path('favos/', views.favos, name='crm_favos'),
    path('unfavs/', views.unfavs, name='crm_unfavs'),
    path('downloads/', views.downloads, name='crm_downloads'),
    path('favourites/', views.favourites, name='crm_favourites'),
    path('favorisations/', views.favorisations, name='crm_favorisations'),
    path('unfavorisations/', views.unfavorisations, name='crm_unfavorisations'),
    path('newsletters/', views.newsletters, name='crm_newsletters'),

    path('search_queries/', views.SearchQueryListView.as_view(), name='search_queries_list'),
    path('search_queries/<uuid:pk>/', views.SearchQueryDetailView.as_view(), name='search_queries_detail')
]