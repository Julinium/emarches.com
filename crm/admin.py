from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Contacting, Spamming, Favorisation, Unfavorisation, SearchQuery
from portal.models import UserDownloadFile, Profile, Categorie, Procedure, Plan, Payment, Subscription

@admin.register(Contacting)
class ContactingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'replied', 'date_submitted')
    list_filter = ('replied', 'date_submitted')
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-date_submitted',)


@admin.register(Spamming)
class SpammingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'honeypot', 'date_submitted', 'ip_address', 'user_agent')
    list_filter = ('date_submitted',)
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-date_submitted', 'ip_address',)


@admin.register(Favorisation)
class FavorisationAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'date_faved', 'user')
    list_filter = ('date_faved',)
    search_fields = ('consultation', 'user')
    ordering = ('-date_faved', 'consultation', 'user',)


@admin.register(Unfavorisation)
class UnfavorisationAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'date_unfaved', 'user')
    list_filter = ('date_unfaved',)
    search_fields = ('consultation', 'user')
    ordering = ('-date_unfaved', 'consultation', 'user',)


@admin.register(UserDownloadFile)
class UserDownloadFileAdmin(admin.ModelAdmin):
    list_display = ('get_related_ob', 'date_started', 'file_name', 'file_size', 'user')
    list_filter = ('date_started',)
    search_fields = ('user', 'file_name')
    ordering = ('-date_started', 'consultation', 'user',)

    def get_related_ob(self, obj):
        related = obj.related
        if related:
            url = reverse('portal_con_details', args=[related.id])  # Adjust the URL name and args as needed
            return format_html('<a href="{}">{}</a>', url, related)
        return "N/A"

    get_related_ob.short_description = 'Consultation Object'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'role', 'email', 'phone')
    search_fields = ('user', 'company', 'ice', 'note', )
    ordering = ('company', 'user',)


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = (
        'date_submitted', 'queryterms', 'results_count', 
        'get_category', 'get_procedure', #'query_results_per_page', 'query_electronic_response', 'query_order_by', 
        'user', 'ip_address', 'user_agent', 
        )
    search_fields = ('user', 'queryterms',)
    ordering = ('-date_submitted', 'user', 'ip_address', 'results_count',)

    @admin.display(description='category')  # Rename the column header
    def get_category(self, obj):
        try: return Categorie.objects.filter(id=obj.query_category).first()
        except: return '-'

    @admin.display(description='procedure')  # Rename the column header
    def get_procedure(self, obj):
        try: return Procedure.objects.filter(id=obj.query_procedure).first()
        except: return '-'

        # return obj.foreign_key_field.name if obj.foreign_key_field else "-"  # Handle None case


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'max_downloads_monthly', 'support_phone_direct', 'support_whatsapp')
    list_filter = ('active', 'support_phone_direct',)
    search_fields = ('name', )
    ordering = ('-active', 'name',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'verified', 'made_date', 'amount', 'refunded')
    list_filter = ('verified', 'refunded', 'made_date',)
    search_fields = ('profile', )
    ordering = ('-made_date', 'amount',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('plan', 'active', 'start_date', 'end_date', 'payment')
    list_filter = ('active',)
    search_fields = ('plan', 'payment')
    ordering = ('-active', '-end_date',)