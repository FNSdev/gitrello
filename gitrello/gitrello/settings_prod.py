import ast

from google.oauth2 import service_account

from gitrello.settings import *

ALLOWED_HOSTS = [
    '127.0.0.1',
    'gitrello.me',
    'www.gitrello.me',
    'gitrello',
]

# Mailing

DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Static
STATIC_URL = f'https://storage.googleapis.com/{os.getenv("GS_BUCKET_NAME")}/static/'

# Google Cloud Storage

GS_BUCKET_NAME = os.getenv('GS_BUCKET_NAME')
DEFAULT_FILE_STORAGE = 'gitrello.gcloud_storages.GoogleCloudMediaStorage'
STATICFILES_STORAGE = 'gitrello.gcloud_storages.GoogleCloudStaticFilesStorage'
try:
    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
        info=ast.literal_eval(os.getenv('GS_CREDENTIALS')),
    )
except Exception:
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(os.getenv('GS_CREDENTIALS'))
GS_PROJECT_ID = os.getenv('GS_PROJECT_ID')
GS_DEFAULT_ACL = 'publicRead'
