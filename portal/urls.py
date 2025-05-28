from django.contrib import admin
from django.urls import path, include

from . import views, autocomplete

urlpatterns = [
    path('results/', views.cons_list, name='portal_cons_list'),
    path('insights/', views.cons_insights, name='portal_cons_insights'),
    path("details/<str:pk>/", views.con_details, name="portal_con_details"),
    path("pid/<str:pid>/", views.con_portal_details, name="portal_con_portal_details"),
    path("dce/<str:pk>/<str:fn>", views.con_get_file, name="portal_con_get_file"),
    path('favs/', views.cons_favs, name='portal_cons_favs'),
    path('clear_favs/', views.clear_favs, name='portal_clear_favs'),
    path("fav/<str:pk>/", views.con_fav, name="portal_con_fav"),
    path("bdc/", views.bdc_landing, name="portal_bdc_landing"),
    # Auto-complete
    # path("locations/", autocomplete.locations, name="locations"),
]
