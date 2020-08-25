from gitrello.settings import *

SECRET_KEY = 'TEST_SECRET_KEY'

URL = 'http://127.0.0.1:8000'
GITHUB_INTEGRATION_SERVICE_URL = 'http://127.0.0.1:8001'

DATABASES = {
    'default': {
        'ENGINE': 'django_cockroachdb',
        'NAME': os.getenv('DJANGO_DB_NAME') or 'gitrello',
        'USER': os.getenv('DJANGO_DB_USER') or 'gitrello',
        'PASSWORD': os.getenv('DJANGO_DB_PASSWORD'),
        'HOST': os.getenv('DJANGO_DB_HOST') or '127.0.0.1',
        'PORT': os.getenv('DJANGO_DB_PORT') or '26257',
    }
}
