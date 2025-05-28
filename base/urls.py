from django.contrib import admin
from django.urls import path, include

from base import views

urlpatterns = [
    path('', views.home, name='base_home'),
    path('about', views.about, name='base_about'),
    path('legal', views.legal, name='base_legal'),
    path('faqs', views.faqs, name='base_faqs'),
    path('contact', views.contact, name='base_contact'),
    path('contact_success', views.contact_success, name='base_contact_success'),
    path('lockout', views.lockout, name='base_lockout'),
    path('accounts/profile', views.profile, name='base_profile'),
    path('accounts/profile/update', views.update_profile, name='base_profile_update'),
    path('services', views.services, name='base_services'),
    # path('portfolio', views.portfolio, name='base_portfolio'),
]
