from gitrello.settings import *

SECRET_KEY = 'aDFgbU43GTgf@34cxbJhg7gsgd^hdgH%'

DEBUG = True

URL = 'http://127.0.0.1:8000'
GITHUB_INTEGRATION_SERVICE_URL = 'http://127.0.0.1:8001'

# To disable IPython debug messages
LOGGING['loggers']['parso'] = {
    'handlers': ['console_debug'],
    'level': 'INFO',
    'propagate': False,
}

ALLOWED_HOSTS = [
    '127.0.0.1',
]

DATABASES = {
    'default': {
        'ENGINE': 'django_cockroachdb',
        'NAME': 'gitrello',
        'USER': 'gitrello',
        'PASSWORD': 'admin',
        'HOST': '127.0.0.1',
        'PORT': '26257',
    }
}
