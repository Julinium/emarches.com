import math, datetime, re
from django import template
from django.utils.translation import gettext
from django.utils.timesince import timesince
from django.conf import settings
from urllib.parse import urlencode, urlparse, urlunparse

from babel.numbers import format_decimal, format_compact_decimal, format_currency
# from babel.numbers import format_number, format_percent

from emarches import constants

FULL_PERIOD = constants.DEFAULT_DELAY_DAYS_MAX
DANGER_DAYS = FULL_PERIOD / 5

DISPLAY_CURRENCY = 'MAD'

register = template.Library()


def to_local(amount, arg):
    return format_currency(amount, DISPLAY_CURRENCY, locale=arg)


def to_local_0d(amount, arg):
    # res = ''
    try: res = format_currency(amount, '', locale=arg)
    except: res = format_currency(amount, '', locale='en')
    # return format_currency(amount, '', locale=arg)
    return res


def to_round(amount):
    return int(100*amount)/100
    # return format_decimal(amount, locale='en', fraction_digits=str(arg))


def redpath(redays):
    r = int(redays)
    if r < 0 : r = 0
    if r > FULL_PERIOD: r = FULL_PERIOD

    return f'{FULL_PERIOD - r} {r}'

def progress_percent(days=0, max_days=FULL_PERIOD):
    if FULL_PERIOD == 0: return 100
    r = int(days)
    if r < 0 : r = 0
    if r > FULL_PERIOD: r = FULL_PERIOD
    return round(100* r / FULL_PERIOD)

def to_short(amount):
    return format_compact_decimal(amount, format_type="short", locale='en_US', fraction_digits=0)


def to_short_c(amount, arg):
    return format_compact_decimal(amount, format_type="long", locale=arg, fraction_digits=1)


def tintino(days):
    try: d = int(days)
    except: d = 0
    if d > FULL_PERIOD : return 'bg-success-subtle'
    if d < FULL_PERIOD + 1 and d > DANGER_DAYS : return 'bg-warning-subtle'
    if d <= DANGER_DAYS : return 'bg-danger-subtle'


def querize(dict):
    q = ''
    for k in dict:
        if dict[k] != '' : q += f'&{k}={dict[k]}'
    return q


register.filter('localize', to_local)
register.filter('localize0d', to_local_0d)
register.filter('shortify', to_short)
register.filter('shortify_c', to_short_c)
register.filter('roundify', to_round)
register.filter('redpath', redpath)
register.filter('progressino', progress_percent)
register.filter('bg_teint', tintino)
register.filter('querize', querize)


@register.simple_tag
def fullpath():
    return FULL_PERIOD


@register.filter
def parse_iso_date(iso_date_string):
    try:
        return datetime.datetime.fromisoformat(iso_date_string)
    except (ValueError, TypeError):
        return None
        

@register.filter
def time1since(value, arg=None):
    """
    Returns only the first part of the timesince result, considering localization.
    """
    result = timesince(value, arg)
    separator = gettext(",")  # Translated separator
    return result.partition(separator)[0]


@register.filter
def in_group(user, group_name):
    if not user or not group_name: return False
    return user.groups.filter(name=group_name).exists()


@register.filter
def stringify(value):
    return str(value)

@register.filter
def gettify(dictionary, key):
    return dictionary.get(key)

##########################


@register.simple_tag(takes_context=True)
def switch_language_url(context, target_lang):
    LANG_PREFIXES = '|'.join(re.escape(lang_code) for lang_code, _ in settings.LANGUAGES)
    LANG_PATTERN = re.compile(rf'^/({LANG_PREFIXES})(/|$)')
    request = context["request"]
    path = request.path
    query_dict = request.GET.copy()

    # Replace language code if present
    if LANG_PATTERN.match(path):
        path = LANG_PATTERN.sub(f'/{target_lang}\\2', path)

    # Reattach query string if present
    query_string = query_dict.urlencode()
    if query_string:
        return f"{path}?{query_string}"
    return path
