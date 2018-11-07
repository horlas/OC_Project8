import dj_database_url
from pur_beurre.settings import *


DEBUG = True

TEMPLATE_DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['*', 'pbquality.herokuapp.com']


MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)

DATABASES['default'] = db_from_env

