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

if os.getenv('ADSEL_ENV') == 'PROD':
    ALLOWED_USERS_GROUP = 'u_acadev_adsel-prod'

if os.getenv('ADSEL_ENV') == 'EVAL':
    ALLOWED_USERS_GROUP = 'u_acadev_adsel-eval'

if os.getenv("ENV") == "localdev":
    DEBUG = True
