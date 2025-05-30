import random
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from django.db.models import Q, Count, Max, Sum
from django.views.generic import ListView, DetailView

from .models import Contacting, Favorisation, Unfavorisation, SearchQuery
from portal.models import UserDownloadFile, ProfileFavCon, Consultation
from emarches import constants as C

from django.contrib.auth import get_user_model # To get the User model


User = get_user_model() # Get the currently active User model


def is_crm_user(user):
    return user.groups.filter(name='CRM').exists()


def padit(reading, pad=12):
    return f"{reading:0{pad}d}"


@login_required(login_url="account_login")
def leads(request):
    if is_crm_user(request.user):
        leads = Contacting.objects.all().order_by('replied', '-date_submitted')

        paginator = Paginator(leads, 10)
        page_number = request.GET.get("page", 1)
        if not str(page_number).isdigit():
            page_number = 1
        else:
            if int(page_number) > paginator.num_pages: page_number = paginator.num_pages
        page_obj = paginator.page(page_number)
        page_range = list(paginator.get_elided_page_range(number=page_number, on_each_side=1, on_ends=1))

        total_count = Contacting.objects.count()

        context = {
            "total_count": padit(total_count, 10),
            "leads": page_obj,
            "page_range": page_range,
            }

        return render(request, 'crm/leads_list.html', context)
    context = {}

    raise PermissionDenied


@login_required(login_url="account_login")
def lead_edit(request, pk):
    lead = get_object_or_404(Contacting, id=pk)
    if is_crm_user(request.user):
        if request.method == "POST":
            lead.replied = request.POST.get("replied") == "on"
            lead.actions = request.POST.get("actions")
            lead.results = request.POST.get("results")
            lead.notes = request.POST.get("notes")
            lead.save()
            context = {}
            return redirect('crm_leads')
        context = {'lead': lead, }
        return render(request, 'crm/lead_edit.html', context)
    context = {}

    raise PermissionDenied


@login_required(login_url="account_login")
def favos(request):
    if is_crm_user(request.user):
        favos = Favorisation.objects.all().order_by('-date_faved')

        paginator = Paginator(favos, 10)
        page_number = request.GET.get("page", 1)
        if not str(page_number).isdigit():
            page_number = 1
        else:
            if int(page_number) > paginator.num_pages: page_number = paginator.num_pages
        page_obj = paginator.page(page_number)
        page_range = list(paginator.get_elided_page_range(number=page_number, on_each_side=1, on_ends=1))

        context = {
            "favos": page_obj,
            "page_range": page_range,
            }

        return render(request, 'crm/favos_list.html', context)
    context = {}

    raise PermissionDenied


@login_required(login_url="account_login")
def unfavs(request):
    if is_crm_user(request.user):
        unfavs = Unfavorisation.objects.all().order_by('-date_unfaved')

        paginator = Paginator(unfavs, 10)
        page_number = request.GET.get("page", 1)
        if not str(page_number).isdigit():
            page_number = 1
        else:
            if int(page_number) > paginator.num_pages: page_number = paginator.num_pages
        page_obj = paginator.page(page_number)
        page_range = list(paginator.get_elided_page_range(number=page_number, on_each_side=1, on_ends=1))

        context = {
            "unfavs": page_obj,
            "page_range": page_range,
            }

        return render(request, 'crm/unfavs_list.html', context)
    context = {}

    raise PermissionDenied


@login_required(login_url="account_login")
def downloads(request):
    if is_crm_user(request.user):
        last_days = 30
        wassa = datetime.now()
        top_downloads = (
            UserDownloadFile.objects.values("consultation")  # Group by 'category' field
            .annotate(
                download_count=Count("id"),
                last_download_date=Max("date_started"),
            )
            .filter(last_download_date__gte=wassa - timedelta(days=last_days), download_count__gt=0)
            .order_by("-download_count")[:10]
        )

        cons_portal_ids = [con["consultation"] for con in top_downloads]
        cons = Consultation.objects.filter(portal_id__in=cons_portal_ids)
        cons_dict = {con.portal_id: con for con in cons}

        total_count = UserDownloadFile.objects.count()
        total_download_size = UserDownloadFile.objects.aggregate(Sum('file_size'))['file_size__sum'] or 0

        context = {
            "total_count": padit(total_count, 10),
            "top_downloads": top_downloads,
            "last_days" : last_days,
            "total_download_size": total_download_size,
            "cons_dict": cons_dict,
            }

        return render(request, 'crm/downloads_list.html', context)
    context = {}

    raise PermissionDenied


@login_required(login_url="account_login")
def favourites(request):
    if is_crm_user(request.user):

        top_favourites = (
            ProfileFavCon.objects.values("consultation")
            .annotate(
                favourite_count=Count("id"),
                last_favourite_date=Max("date_faved"),
            )
            .filter(favourite_count__gt=0)
            .order_by("-favourite_count")[:10]
        )

        cons_portal_ids = [con["consultation"] for con in top_favourites]
        cons = Consultation.objects.filter(portal_id__in=cons_portal_ids)

        cons_dict = {con.portal_id: con for con in cons}

        total_count = ProfileFavCon.objects.count()

        context = {
            "total_count": padit(total_count, 10),
            "top_favourites": top_favourites,
            "cons_dict": cons_dict,
            }

        return render(request, 'crm/favourites_list.html', context)
    context = {}

    raise PermissionDenied


@login_required(login_url="account_login")
def favorisations(request):
    if is_crm_user(request.user):

        top_favorisations = (
            Favorisation.objects.values("consultation")
            .annotate(
                favorisation_count=Count("id"),
                last_favorisation_date=Max("date_faved"),
            )
            .filter(favorisation_count__gt=0)
            .order_by("-favorisation_count")[:10]
        )

        cons_portal_ids = [con["consultation"] for con in top_favorisations]
        cons = Consultation.objects.filter(portal_id__in=cons_portal_ids)

        cons_dict = {con.portal_id: con for con in cons}

        total_count = Favorisation.objects.count()

        context = {
            "total_count": padit(total_count, 10),
            "top_favorisations": top_favorisations,
            "cons_dict": cons_dict,
            }

        return render(request, 'crm/favorisations_list.html', context)
    context = {}

    raise PermissionDenied


@login_required(login_url="account_login")
def unfavorisations(request):
    if is_crm_user(request.user):

        top_unfavorisations = (
            Unfavorisation.objects.values("consultation")
            .annotate(
                unfavorisation_count=Count("id"),
                last_unfavorisation_date=Max("date_unfaved"),
            )
            .filter(unfavorisation_count__gt=0)
            .order_by("-unfavorisation_count")[:10]
        )

        cons_portal_ids = [con["consultation"] for con in top_unfavorisations]
        cons = Consultation.objects.filter(portal_id__in=cons_portal_ids)

        cons_dict = {con.portal_id: con for con in cons}
        total_count = Unfavorisation.objects.count()

        context = {
            "total_count": padit(total_count, 10),
            "top_unfavorisations": top_unfavorisations,
            "cons_dict": cons_dict,
            }

        return render(request, 'crm/unfavorisations_list.html', context)
    context = {}

    raise PermissionDenied
    #return render(request, 'base/errors/unallowed.html', context)


@login_required(login_url="account_login")
def newsletters(request):
    context = {}
    if is_crm_user(request.user):
        context = {}
        return render(request, 'crm/newsletters_list.html', context)
    context = {}

    raise PermissionDenied


@login_required(login_url="account_login")
def supervision(request):
    context = {}
    if is_crm_user(request.user):
        context = {}
        return render(request, 'crm/supervision.html', context)
    context = {}

    raise PermissionDenied


class SearchQueryListView(LoginRequiredMixin, ListView):
    model = SearchQuery
    template_name = 'searchquery_list.html'
    context_object_name = 'search_queries'
    ordering = ['-date_submitted', 'user', 'ip_address']
    paginate_by = 20


    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.GET.get('user')
        country = self.request.GET.get('country')
        language = self.request.GET.get('language')

        if user_id:
            try: queryset = queryset.filter(user__id=int(user_id))
            except ValueError: pass

        if country: queryset = queryset.filter(ip_country=country)
        if language: queryset = queryset.filter(query_language=language)

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_count'] = padit(SearchQuery.objects.count(), 10)
        context['unique_users'] = User.objects.distinct().order_by('username')
        context['unique_countries'] = SearchQuery.objects.values_list('ip_country', flat=True).distinct().exclude(Q(ip_country__isnull=True) | Q(ip_country__exact='')).order_by('ip_country')

        return context


class SearchQueryDetailView(LoginRequiredMixin, DetailView):
    model = SearchQuery
    template_name = 'crm/searchquery_detail.html'
    context_object_name = 'searchquery'  # Default is 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        searchquery = self.object

        # Extract field names and values dynamically
        context['searchquery_fields'] = [
            (field.verbose_name, getattr(searchquery, field.name))
            for field in searchquery._meta.fields
        ]

        return context
