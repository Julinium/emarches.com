import random
from portal.models import ProfileFavCon, Consultation
from crm.models import Contacting
from django.conf import settings

from django.conf.locale import LANG_INFO
from django.utils.translation import get_language_info
from django.utils.translation import gettext as _

from . views import get_trans_ratio



def pillets(request):

    rounder = 10
    min_ratio = 5

    context = {}

    transes = []

    language_info_list = [
        get_language_info(code) | { 'code': code, }
        for code, name in settings.LANGUAGES
    ]

    for language in language_info_list:
        rounded_ratio =   get_trans_ratio(language['code'])
        try: language['ratio'] = max(rounded_ratio - rounded_ratio % rounder, min_ratio)
        except Exception as xc : print(f'---------------- {str(xc)}')
    sorted_transes = sorted(language_info_list, key=lambda x: x["ratio"], reverse=True)
    
    context['m7'] = str(random.randint(1, 7))
    context['transes'] = sorted_transes

    if request.user.is_authenticated :
        profacs = ProfileFavCon.objects.filter(user=request.user).values("consultation")
        context['user_favs'] = user_favs = Consultation.objects.filter(portal_id__in = profacs)
        context['new_contactings'] = Contacting.objects.filter(replied = False) if request.user.groups.filter(name='CRM').exists() else None

    return context




                      
# [
#     {'bidi': False, 'code': 'en', 'name': 'English', 'name_local': 'English', 'name_translated': 'English'}, 
#     {'bidi': False, 'code': 'zg', 'name': 'Tamazight', 'name_local': 'ⵜⴰⵎⴰⵣⵉⵖⵜ', 'name_translated': 'Tamazight'}, 
#     {'bidi': True, 'code': 'ar', 'name': 'Arabic', 'name_local': 'العربيّة', 'name_translated': 'Arabic'}, 
#     {'bidi': False, 'code': 'fr', 'name': 'French', 'name_local': 'français', 'name_translated': 'French'}, 
#     {'bidi': False, 'code': 'es', 'name': 'Spanish', 'name_local': 'español', 'name_translated': 'Spanish'}, 
#     {'bidi': False, 'code': 'de', 'name': 'German', 'name_local': 'Deutsch', 'name_translated': 'German'}
# ]

                      
                          