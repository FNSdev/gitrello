from gitrello.settings import *

ALLOWED_HOSTS = [
    '127.0.0.1',
    'gitrello.me',
    'www.gitrello.me',
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
