# environment-independent configuration for the application
import os


# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
APPEND_SLASH=True
# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True


# Additional locations of static files
STATICFILES_DIRS = (
    #STATIC,
    #'/home/hclass/webapps/humanpcweb/web/templates/protein',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
) 

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#w$0j#c2w5+g%me=c0xdt)9l@y5-^-^z4er(^ia&gee=2-(h2g'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'web.urls'

TEMPLATE_DIRS = (
    BASE_PATH+'templates',

    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'proteins',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'web.proteins.context_processors.settings2',
)
VALID_PROTEIN_EXTENSIONS=('.pdb1.gz', '.pdb.gz', '.pdb', '.ent')

TOOLS_DIR=os.path.join(BASE_PATH,'../tools/')

PROTEINS_DIR=os.path.join(STATIC_PATH,'proteins/')
PROTEINS_MANUAL_UPLOAD_PATH= os.path.join(BASE_PATH,'../proteins_manual_upload/proteins.zip')
PROTEIN_IMAGES_DIR=os.path.join(PROTEINS_DIR, "images/")
PROTEIN_IMAGES_FORMAT= "jpg"
PROTEIN_IMAGES_SIZE= (600,600)
PROTEIN_THUMBNAILS_DIR=os.path.join(PROTEINS_DIR,"images/thumbnails/")
PROTEIN_THUMBNAILS_FORMAT= "gif"
PROTEIN_THUMBNAILS_SIZE= (100,100)

SESSION_EXPIRE_AT_BROWSER_CLOSE=True
#SESSION_SAVE_EVERY_REQUEST=True
AUTH_PROFILE_MODULE = 'proteins.UserProfile'
game_instances_per_level= 1
levels_per_game=10
max_attempts_per_level = 2
game_instances_generator_module='web.proteins.game.game_instance_generation'
game_instances_generator_klass='ScopGameInstanceGenerator'
game_instances_correct_to_level_up=8
game_type = 'movies'