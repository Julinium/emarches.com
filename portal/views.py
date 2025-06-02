import os, csv, random, re, json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, FileResponse, JsonResponse, Http404

from django.views.decorators.cache import cache_control, never_cache
from datetime import date, datetime, timedelta, timezone
from django.db.models import Sum, F, Q, Case, When, Value, CharField, DateField
from django.db.models.functions import TruncMonth, Concat
from collections import defaultdict, OrderedDict
from django.utils.translation import gettext as _
from django.utils.timezone import now
from uuid import UUID
from decimal import Decimal
from pathlib import Path


from django.conf import settings as C
# from emarches import constants

from . import stats
from . models import Consultation, Profile, ProfileFavCon, UserDownloadFile, Categorie, Procedure, Reglage
from crm.models import Favorisation, Unfavorisation, SearchQuery



@login_required(login_url="account_login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cons_favs(request):

    if request.method != 'GET': return HttpResponse(status=403)

    cons = Consultation.objects.filter(portal_id__in = ProfileFavCon.objects.filter(user=request.user).values("consultation"))
    cons = cons.order_by('date_limite_depot', 'id')

    # In case csv dowload was requested, serve it.
    if len(cons) > 0 :
        if 'dld' in request.GET and request.GET['dld']:
            dld = request.GET['dld']
            if dld == 'csv':
                return cons2csv(request, cons, f'eMarches.com-favs-{str(datetime.now())[:16]}.csv')

    paginator = Paginator(cons, C.ITEMS_PER_PAGE)
    page_number = request.GET.get("page", 1)
    if not str(page_number).isdigit():
        page_number = 1
    else:
        if int(page_number) > paginator.num_pages: page_number = paginator.num_pages
    page_obj = paginator.page(page_number)
    page_range = list(paginator.get_elided_page_range(number=page_number, on_each_side=1, on_ends=1))



    context = {
        "cons": cons,
        "page_obj": page_obj,
        "page_range": page_range,
        }
    if not cons:
        messages.add_message(request, messages.WARNING, _("Your Favourites list is empty"))
        return redirect('portal_cons_list')
    return render(request, "portal/cons-favs.html", context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cons_list(request):

    if request.method != 'GET': return HttpResponse(status=403)
    # Get matching profile
    # profile = None
    # try : profile = Profile.objects.get(user = request.user)
    # except : pass
    # TODO: Read PAST_GRACEFUL_HOURS and other attributes from user profile, if any

    qd = {}
    ct = mn = mx = o = r = c = l = None #, None, None, None, None, None
    cons = Consultation.objects.filter(active = True, cancelled = False)
    cons = cons.filter(date_limite_depot__gte = datetime.now() - timedelta(hours=C.PAST_GRACEFUL_HOURS))
    if 'pr' in request.GET and request.GET['pr']:
        pr = request.GET['pr']
        if pr != '' : cons = cons.filter(procedure_annonce__id = str(pr))
        qd['pr'] = pr

    if 'ct' in request.GET and request.GET['ct']:
        ct = request.GET['ct']
        if ct != '' : cons = cons.filter(categorie__id = str(ct))
        qd['ct'] = ct

    if 'mn' in request.GET and request.GET['mn']:
        mn = request.GET['mn']
        cons = cons.filter(total_estimation__gte = float(mn))
        qd['mn'] = mn

    if 'mx' in request.GET and request.GET['mx']:
        mx = request.GET['mx']
        cons = cons.filter(total_estimation__lte = float(mx))
        qd['mx'] = mx

    if 'dd' in request.GET and request.GET['dd']:
        dd = request.GET['dd']
        ddl = datetime.strptime(dd, "%Y-%m-%d").date()
        cons = cons.filter(date_limite_depot__date__gte = ddl)
        qd['dd'] = dd

    if 'ld' in request.GET and request.GET['ld']:
        ld = request.GET['ld']
        ldl = datetime.strptime(ld, "%Y-%m-%d").date()
        cons = cons.filter(date_limite_depot__date__lte = ldl)
        qd['ld'] = ld

    if 'pdn' in request.GET and request.GET['pdn']:
        pdn = request.GET['pdn']
        pdnl = datetime.strptime(pdn, "%Y-%m-%d").date()
        cons = cons.filter(date_publication__gte = pdnl)
        qd['pdn'] = pdn

    if 'pdx' in request.GET and request.GET['pdx']:
        pdx = request.GET['pdx']
        pdxl = datetime.strptime(pdx, "%Y-%m-%d").date()
        cons = cons.filter(date_publication__lte = pdxl)
        qd['pdx'] = pdx

    # TODO: Split if many words and search with OR
    if 'o' in request.GET and request.GET['o']:
        o = request.GET['o']
        cons = cons.filter(objet__unaccent__icontains = str(o))
        qd['o'] = o

    # TODO: Split if many words and search with OR
    if 'r' in request.GET and request.GET['r']:
        r = request.GET['r']
        cons = cons.filter(reference__unaccent__icontains = str(r))
        qd['r'] = r

    # TODO: Split if many words and search with OR
    if 'c' in request.GET and request.GET['c']:
        c = request.GET['c']
        cons = cons.filter(acheteur_public__nom__unaccent__icontains = str(c))
        qd['c'] = c

    # TODO: Split if many words and search with OR
    if 'l' in request.GET and request.GET['l']:
        l = request.GET['l']
        cons = cons.filter(lieu_execution__unaccent__icontains = str(l))
        qd['l'] = l

    if 're' in request.GET and request.GET['re']:
        re = request.GET['re']
        if re != '' : cons = cons.filter(reponse_electronique = str(re))
        qd['re'] = re

    if 'sl' in request.GET:
        cons = cons.filter(nombre_lots = 1)
        qd['sl'] = 'sl'

    if 'rs' in request.GET:
        cons = cons.filter(lot__reserve_pme = True).distinct()
        qd['rs'] = 'rs'

    ob = 'DL'
    if 'ob' in request.GET and request.GET['ob']:
        ob = request.GET['ob']
    qd['ob'] = ob

    match ob : # dl dp e c
        case 'DL': cons = cons.order_by('date_limite_depot', 'id')
        case '-DL': cons = cons.order_by('-date_limite_depot', 'id')
        case 'DP': cons = cons.order_by('date_publication', 'date_limite_depot', 'id')
        case '-DP': cons = cons.order_by('-date_publication', 'date_limite_depot', 'id')
        case 'TE': cons = cons.order_by('total_estimation', 'date_limite_depot', 'id')
        case '-TE': cons = cons.order_by('-total_estimation', 'date_limite_depot', 'id')
        case 'TC': cons = cons.order_by('caution_provisoire', 'date_limite_depot', 'id')
        case '-TC': cons = cons.order_by('-caution_provisoire', 'date_limite_depot', 'id')
        case '-': cons = cons.order_by('-date_limite_depot', 'id')
        case _: cons = cons.order_by('date_limite_depot', 'id')

    # In case csv dowload was requested, serve it.
    if len(cons) > 0 :
        if 'dld' in request.GET and request.GET['dld']:
            dld = request.GET['dld']
            if dld == 'csv':
                return cons2csv(request, cons, f'eMarches.com-{str(datetime.now())[:16]}.csv')

    IPP = C.ITEMS_PER_PAGE
    if 'pp' in request.GET and request.GET['pp']:
        pp = request.GET['pp']
        try: IPP = int(pp)
        except: pass

    qd['pp'] = IPP

    cats = Categorie.objects.exclude(nom__in = ['', C.NA_PLACE_HOLDER]).order_by('nom')
    procs = Procedure.objects.exclude(nom__in = ['', C.NA_PLACE_HOLDER]).order_by('nom')
    repels = Consultation.objects.order_by('-reponse_electronique').values_list('reponse_electronique', flat=True).distinct('reponse_electronique')
    favs = None
    if request.user.is_authenticated:
        favs = Consultation.objects.filter(portal_id__in = ProfileFavCon.objects.filter(user=request.user).values("consultation"))

    cons_age = None
    try: cons_age = Reglage.objects.all().last().cons_last_update.astimezone()
    except : pass    # print(f'[{datetime.now().strftime("%y-%m-%d %H:%M")}] Exception raised while reading settings: { str(x) }')

    paginator = Paginator(cons, IPP)
    page_number = request.GET.get("page", 1)
    if not str(page_number).isdigit():
        page_number = 1
    else:
        if int(page_number) > paginator.num_pages: page_number = paginator.num_pages
    page_obj = paginator.page(page_number)
    page_range = list(paginator.get_elided_page_range(number=page_number, on_each_side=1, on_ends=1))

    try: logSerachQuery(request, qd, len(cons))
    except: pass

    context = {
        'cons' : cons,
        "page_obj": page_obj,
        "page_range": page_range,
        'qd': qd,
        'cats': cats,
        'procs': procs,
        'repels': repels,
        'favs' : favs,
        'cons_age' : cons_age,

        }
    return render(request, "portal/cons-list.html", context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def con_details(request, pk=None):     # if request.user.is_authenticated:

    if request.method != 'GET': return HttpResponse(status=403)

    try: valid_uuid = UUID(pk, version=4)
    except ValueError: raise Http404("Invalid UUID")

    con = get_object_or_404(Consultation, id=pk)

    faved = None
    if request.user.is_authenticated : faved = ProfileFavCon.objects.filter(user=request.user).filter(consultation=con.portal_id).first()

    files_list = []
    total_size = 0
    dce_dir = os.path.join(os.path.join(C.MEDIA_ROOT, 'dce'), C.DL_PATH_PREFIX + con.portal_id)
    if os.path.exists(dce_dir): files_list = os.listdir(dce_dir)
    if len(files_list) > 0:
        for f in files_list: total_size += os.path.getsize(os.path.join(dce_dir, f))



    context = {
        "con": con,
        "dlink": con.portal_link,
        'faved': faved,
        'dsize': total_size,
        'flist' : files_list,
        'dce_dir': dce_dir,
        }

    return render(request, "portal/con-details.html", context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def con_portal_details(request, pid=None):     # if request.user.is_authenticated:

    if request.method != 'GET': return HttpResponse(status=403)

    # try: valid_uuid = UUID(pk, version=4)
    # except ValueError: raise Http404("Invalid UUID")

    con = get_object_or_404(Consultation, portal_id=pid)

    faved = None
    if request.user.is_authenticated : faved = ProfileFavCon.objects.filter(user=request.user).filter(consultation=con.portal_id).first()

    files_list = []
    total_size = 0
    dce_dir = os.path.join(os.path.join(C.MEDIA_ROOT, 'dce'), C.DL_PATH_PREFIX + con.portal_id)
    if os.path.exists(dce_dir): files_list = os.listdir(dce_dir)
    if len(files_list) > 0:
        for f in files_list: total_size += os.path.getsize(os.path.join(dce_dir, f))



    context = {
        "con": con,
        "dlink": con.portal_link,
        'faved': faved,
        'dsize': total_size,
        'flist' : files_list,
        'dce_dir': dce_dir,
        }

    return render(request, "portal/con-details.html", context)


@login_required(login_url="account_login")
def con_fav(request, pk=None):

    if request.method != 'GET': return HttpResponse(status=403)

    con = Consultation.objects.get(id=pk)
    if con is None: return HttpResponse(status=410)


    sc = 200

    profacs = ProfileFavCon.objects.filter(user=request.user).filter(consultation=con.portal_id)
    if len(profacs) > 0:
        for profac in profacs:
            profac.delete()
            favo = Unfavorisation(
                consultation    = con.portal_id,
                user            = request.user,
            )
            favo.save()
    else:
        profac = ProfileFavCon(
            consultation    = con.portal_id,
            user            = request.user,
            date_faved      = datetime.now(),
            # note_faved      = '',
        )
        profac.save()
        unfa = Favorisation(
            consultation    = con.portal_id,
            user            = request.user,
        )
        unfa.save()

        sc = 201

    return HttpResponse(status=sc)

    # 200 - OK                      ===== Removed from Favs
    # 201 – Created                 ===== Added to Favs
    # 304 – resource not modified   =====
    # 410 - Gone


@login_required(login_url="account_login")
def clear_favs(request):

    if request.method != 'GET': return HttpResponse(status=403)
    rescode = 304
    profacs = ProfileFavCon.objects.filter(user=request.user)
    if len(profacs) > 0 :
        if 'sco' in request.GET and request.GET['sco']:
            sco = request.GET['sco']
            if sco == 'unfavourite-all':
                try:
                    for profac in profacs:
                        con = Consultation.objects.get(portal_id=profac.consultation)
                        profac.delete()
                        unfa = Unfavorisation(
                            consultation    = con.portal_id,
                            user            = request.user,
                        )
                        unfa.save()
                except: rescode = 410
                rescode = 200
            else:
                try:
                    i = 0
                    for profac in profacs:
                        con = Consultation.objects.get(portal_id=profac.consultation)
                        if con:
                            if con.date_limite_depot < datetime.now(timezone.utc):
                                i += 1
                                profac.delete()
                                unfa = Unfavorisation(
                                    consultation    = con.portal_id,
                                    user            = request.user,
                                )
                                unfa.save()
                    if i > 0 : rescode = 200
                except Exception as x:
                    print(str(x))
                    rescode = 410

    if rescode == 200 : messages.add_message(request, messages.SUCCESS, _('Favourites cleared succcessfully'))
    return HttpResponse(status=rescode)


@login_required(login_url="account_login")
def con_get_file(request, pk=None, fn=None):

    if request.method != 'GET': return HttpResponse(status=403)
    if pk == None or fn == None: return HttpResponse(status=404)

    con = Consultation.objects.get(id=pk)
    if not con : return HttpResponse(status=404)

    dce_dir = os.path.join(os.path.join(C.MEDIA_ROOT, 'dce'), C.DL_PATH_PREFIX + con.portal_id)
    file_fp = os.path.join(dce_dir, fn)

    if os.path.exists(file_fp):

        user_agent = request.META.get('HTTP_USER_AGENT', '')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for: user_ip = x_forwarded_for.split(',')[0]
        else: user_ip = request.META.get('REMOTE_ADDR', '')

        udf = UserDownloadFile(
            consultation = con.portal_id,
            user = request.user,
            user_agent = user_agent,
            user_ip = user_ip,
            file_name = os.path.basename(file_fp),
            file_size = os.path.getsize(file_fp),
            )
        udf.save()

        with open(file_fp, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/zip")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_fp)
            return response
    return HttpResponse(status=500)


def cons_insights(request):

    period_length = 'months'
    if 'period' in request.GET and request.GET['period']:
        period_length = request.GET['period']

    if not period_length in ['weeks', 'months', 'quarters', 'years']: period_length = 'months'

    match period_length:
        case 'weeks':
            past_offset = 8
            future_offset = 4
        case 'quarters':
            past_offset = 8
            future_offset = 3
        case 'years':
            past_offset = 7
            future_offset = 2
        case _:
            past_offset = 8
            future_offset = 3


    periods = stats.generate_periods(past_offset, future_offset, period_length)
    if len(periods) == 0: return render(request, 'base/includes/empty.html', context)

    today = datetime.today()

    start_date = periods[0]['start_date']#.get('start_date', today)
    final_date = periods[-1]['end_date']#.get('end_date', today)

    if not start_date or not final_date: return render(request, 'base/includes/empty.html', context)
    if start_date == final_date: return render(request, 'base/includes/empty.html', context)

    consultations = Consultation.objects.filter(
        active=True,
        cancelled=False,
        date_limite_depot__gte=start_date,
        date_limite_depot__lte=final_date
        )
    if len(consultations) == 0: return render(request, 'base/includes/empty.html', context)

    grand_count = len(consultations)
    grand_total = consultations.aggregate(total=Sum('total_estimation'))['total']
    if grand_total is None: grand_total = 0


    # if period_length == 'months':
    #     file_path = os.path.join(os.path.dirname(__file__), 'months.json')

    #     # Read and parse the JSON data
    #     with open(file_path, 'r') as json_file:
    #         ordered_data = json.load(json_file)
    # else:
    period_filters = Q()
    case_statements = []
    start_date_statements = []

    for period in periods:
        # Add the period range to the filter
        period_filters |= Q(
            date_limite_depot__gte=period['start_date'],
            date_limite_depot__lte=period['end_date']
        )

        # Add a case statement for assigning labels to the periods
        case_statements.append(
            When(
                date_limite_depot__gte=period['start_date'],
                date_limite_depot__lte=period['end_date'],
                then=Value(period['label'])
            )
        )

        # Add a case statement for assigning the start_date to the periods
        start_date_statements.append(
            When(
                date_limite_depot__gte=period['start_date'],
                date_limite_depot__lte=period['end_date'],
                then=Value(period['start_date'])
            )
        )

    # Query the data
    categorie_totals = consultations.filter(period_filters).annotate(
        period_label=Case(
            *case_statements,
            output_field=CharField()
        ),
        period_start_date=Case(
            *start_date_statements,
            output_field=DateField()  # Use DateField for start_date
        )
    ).values(
        'period_label', 'period_start_date', 'categorie__nom'
    ).annotate(
        total_amount=Sum('total_estimation')
    ).order_by(
        'period_start_date', 'categorie__nom'
    )


    # Organize data for the doughnut chart by period_label
    categorie_data = defaultdict(lambda: defaultdict(float))
    for entry in categorie_totals:
        categorie_data[entry['period_label']][entry['categorie__nom']] += float(entry['total_amount'] or Decimal(0))

    doughnut_chart_data = {}
    for period_label, categories in categorie_data.items():
        doughnut_chart_data[period_label] = {
            'labels': list(categories.keys()),
            'datasets': [{
                'data': list(categories.values()),
            }]
        }

    ordered_data = [dict(doughnut_chart_data)]

    try:
        latest_record = Consultation.objects.latest('date_limite_depot')
        epoch_stop = latest_record.date_limite_depot.replace(tzinfo=None)
    except : pass

    try:
        first_record = Consultation.objects.order_by('date_limite_depot').first()
        epoch_zero = first_record.date_limite_depot.replace(tzinfo=None)
    except : pass


    start_date = max(start_date, epoch_zero.date())
    final_date = min(final_date, epoch_stop.date())


    days_delta = final_date - start_date
    days_count = days_delta.days
    daily_mean = grand_total / days_count if days_count != 0 else 0
    month_mean = 30 * daily_mean
    daily_count = grand_count / days_count if days_count != 0 else 0


    context = {
        'start_date': start_date,
        'final_date': final_date,
        'period' : period_length,
        'daily_count' : daily_count,
        'grand_count' : grand_count,
        'grand_total' : grand_total,
        'days_count' : days_count,
        'daily_mean' : daily_mean,
        'month_mean' : month_mean,
        'doughnut_charts': ordered_data,
    }

    return render(request, 'portal/cons_insights.html', context)


def bdc_landing(request):
    return render(request, 'portal/bdc-landing.html', {})



# Functions ...

def cons2csv(request, cons, filename):

    if not request.user.is_authenticated :
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="eMarches.com-unallowed.csv"'
        writer = csv.writer(response)
        writer.writerow([_('This file is only for authenticated users and you should not have accessed it.')])
        writer.writerow([_('Our servers security mechanism replaced the original content with this message.')])
        writer.writerow([_('If you got this file from our servers, we would like to know how you did.')])
        writer.writerow([_('We may hire you. Please contact us. Links on eMarches.com')])
        return response

    from djqscsv import render_to_csv_response
    base_url = "https://www.emarches.com/en/cons/details/"
    return render_to_csv_response(cons.annotate(url=Concat( Value(base_url), 'id', Value("/"), output_field=CharField())).values(
        'date_publication__date', 'date_limite_depot', 'reference', 'categorie__nom',
        'total_estimation', 'caution_provisoire', 'nombre_lots', 'objet', 'lieu_execution',
        'acheteur_public__nom', 'procedure_annonce__nom', 'mode_passation__nom', 'reponse_electronique',
        'retrait_dossiers_adresse', 'depot_offres_adresse', 'ouverture_plis_adresse', 'url',),
        field_header_map={
            'categorie__nom' : 'categorie',
            'date_publication__date' : 'date publication',
            'acheteur_public__nom': 'acheteur public',
            'procedure_annonce__nom': 'procedure',
            'mode_passation__nom': 'mode_passation',
            'url': 'lien eMArches',
            # 'portal_link' : 'lien PMMP',
            },
        filename=filename,
        )


def logSerachQuery(request, querydict, results_count):    
   
    import geoip2.database

    user_agent = request.META.get('HTTP_USER_AGENT', '')
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for: ip_address = x_forwarded_for.split(',')[0]
    else: ip_address = request.META.get('REMOTE_ADDR', '')

    user = None
    if request.user.is_authenticated : user = request.user

    geoip_db = f"{C.BASE_DIR}/geoip/GeoLite2-City.mmdb"
    reader = geoip2.database.Reader(geoip_db)

    ip_country, ip_cc_iso, ip_city, ip_latitude, ip_longitude = None, None, None, None, None

    try:
        response = reader.city(ip_address)
        ip_country   = response.country.name
        ip_cc_iso    = response.country.iso_code
        ip_city      = response.city.name
        ip_latitude  = response.location.latitude
        ip_longitude = response.location.longitude
    except geoip2.errors.AddressNotFoundError:
        print(f"No entry for {ip_address} in the database.")
    finally:
        reader.close()

    search_query = SearchQuery(

        query_full_url  = request.build_absolute_uri(),
        query_hostname  = request.get_host(),
        query_full_path = request.get_full_path(),
        query_language  = request.LANGUAGE_CODE,

        query_object = querydict.get('o', None),
        query_reference = querydict.get('r', None),
        query_estimate_min = querydict.get('mn', None),
        query_estimate_max = querydict.get('mx', None),
        query_category = querydict.get('ct', None),
        query_procedure = querydict.get('pr', None),
        query_deadline_min = querydict.get('dd', None),
        query_deadline_max = querydict.get('ld', None),
        query_published_min = querydict.get('pdn', None),
        query_published_max = querydict.get('pdx', None),
        query_client = querydict.get('c', None),
        query_execution_location = querydict.get('l', None),
        query_electronic_response = querydict.get('re', None),
        query_single_lot_only = True if querydict.get('sl', None) else False,
        query_reserved_to_smb = True if querydict.get('rs', None) else False,
        query_results_per_page = querydict.get('pp', None),
        query_order_by = querydict.get('ob', None),

        results_count = results_count,
        user         = user,
        user_agent   = user_agent,
        ip_address   = ip_address,
        ip_country   = ip_country,
        ip_cc_iso    = ip_cc_iso,
        ip_city      = ip_city,
        ip_latitude  = ip_latitude,
        ip_longitude = ip_longitude,
    )
    search_query.save()
