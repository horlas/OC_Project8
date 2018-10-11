import dj_database_url
from pur_beurre.settings import *


DEBUG = False

TEMPLATE_DEBUG = False

SECRET_KEY = ')(v10co96cxd@d^k+gnefi_jw_boavod*x(uzxkw-k+x!)y1^@'

ALLOWED_HOSTS = ['*', 'pbquality.herokuapp.com']


MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



db_from_env = dj_database_url.config(conn_max_age=500)

DATABASES['default'] = dj_database_url.config()