from .base_settings import *

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'webpack_loader',
    'cohort_manager',
]

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'cohort_manager/bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'cohort_manager', 'static', 'webpack-stats.json'),
    }
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'debug':  True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    }
]

if os.getenv('ENV') == 'prod':
    ALLOWED_USERS_GROUP = 'u_acadev_adsel-prod'
elif os.getenv('ENV') == 'eval':
    ALLOWED_USERS_GROUP = 'u_acadev_adsel-eval'
else:
    ALLOWED_USERS_GROUP = 'u_test_group'

if os.getenv('ADSEL_ENV') == 'PROD' or os.getenv('ADSEL_ENV') == 'EVAL':
    RESTCLIENTS_ADSEL_DAO_CLASS = 'Live'
    RESTCLIENTS_ADSEL_TIMEOUT = 120
    RESTCLIENTS_ADSEL_POOL_SIZE = 10
    RESTCLIENTS_ADSEL_CERT_FILE = APPLICATION_CERT_PATH
    RESTCLIENTS_ADSEL_KEY_FILE = APPLICATION_KEY_PATH

if os.getenv('ADSEL_ENV') == 'PROD':
    RESTCLIENTS_ADSEL_HOST = 'https://adselapi.uw.edu'

if os.getenv('ADSEL_ENV') == 'EVAL':
    RESTCLIENTS_ADSEL_HOST = 'https://test.adselapi.uw.edu' 

if os.getenv("ENV") == "localdev":
    DEBUG = True
