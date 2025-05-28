import os, argparse, django.conf.locale, json
from pathlib import Path
from django.conf import global_settings
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

# Load the .env file from parent directory
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG_MODE") == "True"


ALLOWED_HOSTS = ['www.emarches.com', 'emarches.com', 'localhost' , '127.0.0.1', ]

CSRF_TRUSTED_ORIGINS = ['https://www.emarches.com', 'https://emarches.com', ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.postgres', # Needed for unaccent extension.

    'base',
    'crm',
    'portal',

    'dotenv',
    'djqscsv',
    'allauth',
    'allauth.account',
    'widget_tweaks',
    'requests',
    'slugify',
    'bs4',
    'axes',
    'django_countries',
    'bootstrap_admin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    "allauth.account.middleware.AccountMiddleware",
    'axes.middleware.AxesMiddleware',
]

SITE_ID = 1

DEFAULT_DOMAIN  = "emarches.com"
ROOT_URLCONF    = 'emarches.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'base.context_processors.pillets',
                'django.template.context_processors.media',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # AxesStandaloneBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesStandaloneBackend',

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'emarches.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'HOST':     os.getenv("DB_HOST"),
        'PORT':     os.getenv("DB_PORT"),
        'NAME':     os.getenv("DB_NAME"),
        'USER':     os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASS"),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Time zone and languages
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Add support for non-standardized language
EXTRA_LANG_INFO = {
    'zg': {
        'bidi': False, # right-to-left ?
        'code': 'zg',
        'name': 'Tamazight',
        'name_local': 'ⵜⴰⵎⴰⵣⵉⵖⵜ', #unicode codepoints
    },
}

LANG_INFO = {**django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO}
django.conf.locale.LANG_INFO = LANG_INFO

LANGUAGES = [
    ("en", _("English")),
    ("zg", _("Amazigh")),
    ("ar", _("Arabic")),
    ("fr", _("French")),
    ("es", _("Spanish")),
    ("de", _("German")),
    ]
    
LOCALE_PATHS = [BASE_DIR / "locale", ]
USE_THOUSAND_SEPARATOR = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django_allauth parameters
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'base_home'
LOGOUT_REDIRECT_URL = 'portal_cons_favs'
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CHANGE_EMAIL = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_SUBJECT_PREFIX = 'eMarches - '
ACCOUNT_SIGNUP_FORM_HONEYPOT_FIELD = 'age'
ACCOUNT_USERNAME_BLACKLIST = ['admin', 'owner', 'wassim', 'm777', 'mode777', 'mode-777', 'emarches', 'root', 'insi', 'system']
ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_USERNAME_VALIDATORS = 'base.validators.username_ASCII_validators'
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
# ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED = True
# ACCOUNT_EMAIL_VERIFICATION_BY_CODE_MAX_ATTEMPTS = 5
# ACCOUNT_EMAIL_VERIFICATION_BY_CODE_TIMEOUT = 900
# ACCOUNT_EMAIL_NOTIFICATIONS = True

# Axes parameters
AXES_FAILURE_LIMIT = 5# Number of failed login attempts before blocking
AXES_COOLOFF_TIME = 1# Period before failed attempts are reset (in hours)
AXES_IGNORE_USERNAME = ['socialaccount_user']# Prevent detection of "failed" logins for password-less (e.g., social) logins
AXES_LOCKOUT_URL = 'base_lockout' # Redirect URL for lockouts
AXES_LOGGING = True# Optional: Store logs for audit purposes

# Coloring messages for UI styling
MESSAGE_TAGS = {
        messages.DEBUG: 'secondary',
        # messages.INFO: 'alert-info',
        # messages.SUCCESS: 'alert-success',
        # messages.WARNING: 'alert-warning',
        messages.ERROR: 'danger',
 }


# Email backend parameters
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True
EMAIL_HOST          = os.getenv("EMAIL_HOST")
EMAIL_PORT          = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER     = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL  = os.getenv("DEFAULT_FROM_EMAIL")


COUNTRIES_FIRST = ['MA', 'FR', 'US',]
