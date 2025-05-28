# import random, re, os
# from django.conf import settings
# from slugify import slugify
# import requests
# from bs4 import BeautifulSoup


# DEFAULT_UA = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'

# USER_AGENTS = [
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
#     'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
#     'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
#     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
#     'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
# ]

# HOME_DIR = settings.BASE_DIR

# def getDCE(clink):
#     if not os.path.exists(HOME_DIR): return None
#     if not clink : return None
#     if len(clink) < 5 : return None

#     pide = clink.strip('https://www.marchespublics.gov.ma/index.php?page=entreprise.EntrepriseDetailsConsultation&refConsultation=')
#     pid = pide.split('&orgAcronym')[0]
#     if len(pid) < 1: return None

#     con_path = HOME_DIR / f'media/dce/{pid}'
#     if not os.path.exists(con_path): os.makedirs(con_path)
#     if not os.path.exists(con_path): return None
    
#     PAGEQ = 'entreprise.EntrepriseDetailsConsultation'
#     PAGED = 'entreprise.EntrepriseDemandeTelechargementDce'
#     PAGEF = 'entreprise.EntrepriseDownloadCompleteDce'

#     if len(USER_AGENTS) == 0 : headino = {"User-Agent": DEFAULT_UA}
#     else : headino = {"User-Agent": USER_AGENTS[random.randint(0, len(USER_AGENTS)-1)]}

#     sessiono = requests.Session()

#     urlq = clink.replace('entreprise.EntrepriseDetailConsultation', 'entreprise.EntrepriseDemandeTelechargementDce')
#     rq = sessiono.get(urlq, headers=headino)
#     if settings.DEBUG: print(f'Getting Link : {rq}')
#     rcode = rq.status_code
#     if rcode != 200 : return rcode

#     soup = BeautifulSoup(rq.content, 'html5lib')

#     prado_page_state = soup.find(id="PRADO_PAGESTATE")['value']
#     prado_pbk_target = soup.find(id="PRADO_POSTBACK_TARGET")['value']
#     prado_pbk_parame = soup.find(id="PRADO_POSTBACK_PARAMETER")['value']

#     datano = {
#         'PRADO_PAGESTATE': prado_page_state,
#         'PRADO_POSTBACK_TARGET': prado_pbk_target,
#         'PRADO_POSTBACK_PARAMETER': prado_pbk_parame,
#         'ctl0$CONTENU_PAGE$EntrepriseFormulaireDemande$nom': 'ZAHIR',
#         'ctl0$CONTENU_PAGE$EntrepriseFormulaireDemande$prenom': 'Zahir',
#         'ctl0$CONTENU_PAGE$EntrepriseFormulaireDemande$email': 'h.zahir@menara.ma', 
#     }

#     urld = urlq
#     rd = sessiono.get(urld, headers=headino, data=datano)
#     if settings.DEBUG: print(f'Submitting form : {rd}')
#     rcode = rd.status_code
#     if rcode != 200 : return rcode

#     urlf = urld.replace('entreprise.EntrepriseDemandeTelechargementDce', 'entreprise.EntrepriseDownloadCompleteDce').replace('refConsultation', 'reference').replace('orgAcronyme', 'orgAcronym')
    
#     if settings.DEBUG: print(f'Cons link : {urlq}')
#     if settings.DEBUG: print(f'Form link : {urld}')
#     if settings.DEBUG: print(f'File link : {urlf}')
#     rf = sessiono.get(urlf)
#     if settings.DEBUG: print(f'Getting file : {rf}')
#     rcode = rf.status_code
#     if rcode != 200 : return rcode

#     def get_filename(cd):
#         if not cd:
#             return None
#         fname = re.findall('filename=(.+)', cd)
#         if len(fname) == 0:
#             return None
#         return fname[0]

#     filename_cd = slugify(get_filename(rf.headers.get('content-disposition'))).strip('-zip')
#     filename = con_path / f'eMarches.com-{filename_cd}.zip'
#     if settings.DEBUG: print(filename)
#     open(filename, 'wb').write(rf.content)

#     return os.path.abspath(filename)
