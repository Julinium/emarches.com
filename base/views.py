import os, random, threading
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage

from django.utils.translation import gettext as _
from django.utils import translation
from django.contrib import messages
from datetime import datetime as dt


from portal.models import Profile, Plan, Payment, Subscription
from crm.models import Contacting

from .forms import ProfileUpdateForm

from pathlib import Path
import polib



def get_client_ip(request):
    ip = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR') # Check for the forwarded IP header first
    if x_forwarded_for: ip = x_forwarded_for.split(',')[0] # In case of multiple addresses, the first is the client IP
    else: ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR') # Fallback to X-Real-IP or remote address
    return ip

def get_user_agent(request):
    return request.META.get('HTTP_USER_AGENT', 'Unknown')

def get_trans_ratio(language_code):
    """
    Calculate the ratio of translated strings for a given language in a Django project using polib.
    Args:
        language_code (str): The language code (e.g., 'fr', 'es', 'de').
    """

    # Get the locale directory path
    if language_code == 'en': return 100

    locale_path = Path(settings.BASE_DIR) / "locale" / language_code / "LC_MESSAGES"
    po_file_path = locale_path / "django.po"
    if not po_file_path.exists(): return 0
    po_file = polib.pofile(po_file_path)
    total_strings = len([entry for entry in po_file])
    untranslated = len([entry for entry in po_file if not entry.translated()])

    if total_strings == 0: return 0
    return  int(((total_strings - untranslated) / total_strings) * 100)


def home(request):    
    scripts = [
        {'image': 'search',     'name': 'search',     'header': _('Advanced Search'),        'detail': _('Easily find the exact tender that matches your business goals')},
        {'image': 'download',   'name': 'download',   'header': _('Effortless Downloads'),   'detail': _('Download files for promising opportunities in just two clicks')},
        {'image': 'favourite',  'name': 'favourite',  'header': _('Save Your Favorites'),    'detail': _('Mark tenders as favorites for quick and easy access later')},
        {'image': 'responsive', 'name': 'responsive', 'header': _('Responsive Design'),      'detail': _('Our elegant interface adapts seamlessly to any screen size')},
        {'image': 'languages',  'name': 'languages',  'header': _('Multi-Language'),         'detail': _('Choose from Arabic, Tamazight, English, French, or Spanish')},
        {'image': 'services',   'name': 'services',   'header': _('Free Services'),          'detail': _('Enjoy all our services completely free of charge')},
        {'image': 'incoming',   'name': 'incoming',   'header': _('Exciting Updates'),       'detail': _('We’re just getting started. More amazing features are coming soon')}
    ]

    context = {
        'scripts' : scripts,
    }

    return render(request, 'base/home.html', context)


def about(request):
    context = {}
    # transes = []
    # for lang_code, lang_name in settings.LANGUAGES:
    #     try: transes.append({'code': lang_code, 'name': lang_name, 'ratio': get_trans_ratio(lang_code), })
    #     except Exception as xc : print(f'---------------- {str(xc)}')
    # sorted_transes = sorted(transes, key=lambda x: x["ratio"], reverse=True)
    # context = {
    #     'transes' : sorted_transes,
    #     }
    return render(request, 'base/about.html', context)


def legal(request):
    context = {}
    return render(request, 'base/legal.html', context)


def faqs(request):
    context = {}
    return render(request, 'base/faqs.html', context)


def services(request):
    context = {}
    return render(request, 'base/services.html', context)


def contact(request):

    def send_client_email(destination, instance, language_code='en', fm='no-reply@emarches.com'):
        translation.activate(language_code)
        subject = 'eMarches - ' + _('Message submitted')
        plain_message = render_to_string('base/emails/submitted.txt', {'instance': instance})
        html_message = render_to_string('base/emails/submitted.html', {'instance': instance})        
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,   # Plain-text content
            from_email=fm,
            to=[destination],     # Recipient list
        )
        email.attach_alternative(html_message, "text/html")  # Attach HTML content 
        translation.deactivate()
        return email.send()
    
    def send_crm_email(destination, instance, fm='no-reply@emarches.com'):
        email_body = _('Some one submitted a message on eMarches.com using Contact form')  + '.\n\n'
        email_body += _('Name') + f' : { instance.name }\n'
        email_body += _('Email') + f' : { instance.email }\n'
        email_body += _('Phone') + f' : { instance.phone }\n'
        email_body += _('Subject') + f' : { instance.subject }\n'
        email_body += _('Message') + f' : { instance.message }\n'
        email_body += _('Prefferred contact method') + f' : { instance.contact_method }\n'
        email_body += _('Subscribe to Newsletter') + f' : { instance.subscribe_newsletter } \n'
        email_body += _('Subscribe to Offers') + f' : { instance.subscribe_promotions } \n'
        email_body += _('Submitted on') + f' : { instance.date_submitted } \n'
        email_subject = 'eMarches - ' + _('New Contact')
        return send_mail(email_subject, email_body, fm, [destination])
    
    context = {}

    if request.method == "POST":
        try:
            honeypot = request.POST.get('thammnn', '')
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            subject = request.POST['subject']
            message = request.POST['message']
            contact_method = request.POST.get('contact_method', 'any')
            subscribe_newsletter = request.POST.get('subscribe_newsletter') == 'on'
            subscribe_promotions = request.POST.get('subscribe_promotions') == 'on'
            user = request.user if request.user.is_authenticated else None
            ip_address = get_client_ip(request)
            user_agent = get_user_agent(request)

            if honeypot == '':
                contacting = Contacting(
                    name = name,
                    email = email,
                    phone = phone,
                    subject = subject,
                    message = message,
                    contact_method = contact_method,
                    subscribe_newsletter = subscribe_newsletter,
                    subscribe_promotions = subscribe_promotions,
                    user = user,
                    ip_address = ip_address,
                    user_agent = user_agent,
                )
                contacting.save()
                # Start a new thread to send the email
                try:
                    thread_client = threading.Thread(target=send_client_email, args=(email, contacting, request.LANGUAGE_CODE, ))
                    thread_crm = threading.Thread(target=send_crm_email, args=('a.bouhou@emarches.com', contacting, ))
                    thread_client.start()
                    thread_client.join()
                    thread_crm.start()
                    # threading.Thread(target=send_client_email, args=(email, contacting, request.LANGUAGE_CODE, )).start()
                except Exception as xc: print(f'xxxxxxxxxxxxxxxxxx {str(xc)}')

            else:
                spamming = Spamming(
                    honeypot = honeypot,
                    name = name,
                    email = email,
                    phone = phone,
                    subject = subject,
                    message = message,
                    contact_method = contact_method,
                    subscribe_newsletter = subscribe_newsletter,
                    subscribe_promotions = subscribe_promotions,
                    user = user,
                    ip_address = ip_address,
                    user_agent = user_agent,
                )
                spamming.save()
            messages.add_message(request, messages.SUCCESS, _("Submitted. Thank you for contacting us"))           
            return render(request, 'base/contact_success.html')
        except Exception as xc:
            print(f'Exception raised while getting request data:')
            print(f'xxxxxxxxxxxxxxxxxx {str(xc)}')
            messages.add_message(request, messages.ERROR, _("Something went wrong"))
            return render(request, 'base/errors/5xx.html')
    return render(request, 'base/contact.html', context)


def contact_success(request):
    context = {}
    return render(request, 'base/contact_success.html', context)


def lockout(request):
    context = {}
    return render(request, 'base/lockout.html', context)


@login_required(login_url="account_login")
def profile(request):
        
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        if profile:
            payments        = Payment.objects.filter(profile=profile, refunded=False, verified=True)
            subscriptions   = Subscription.objects.filter(active=True, payment__in=payments)

            wassa = dt.now()
            active_sub = subscriptions.filter(start_date__lte=wassa, end_date__gte=wassa).first()

            plan = None
            remaining_days = 0
            if active_sub:
                plan = active_sub.plan
                assa = dt.today()
                remaining_days = active_sub.end_date.date() - assa.date()
                remaining_days = remaining_days.days

            context = {
                "payments"       : payments,
                "subscriptions"  : subscriptions,
                "active_sub"     : active_sub,
                "plan"           : plan,
                "remaining_days" : remaining_days,
                }

            return render(request, 'base/profile.html', context)

    return render(request, 'base/errors/unallowed.html', {})


@login_required(login_url="account_login")
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your profile has been updated successfully'))
            return redirect('base_profile')
        else:
            messages.error(request, _('There was an error updating your profile'))
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'base/profile_update.html', {'form': form})


def custom_400_view(request, exception=None):
    context = {}
    return render(request, "base/errors/400.html", context, status=400)
    
def custom_403_view(request, exception=None):
    context = {}
    return render(request, "base/errors/403.html", context, status=403)

def custom_404_view(request, exception=None):
    context = {}
    return render(request, "base/errors/404.html", context, status=404)

def custom_500_view(request, exception=None):
    context = {}
    return render(request, "base/errors/500.html", context, status=500)
