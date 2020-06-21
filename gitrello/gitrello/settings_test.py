from gitrello.settings import *

SECRET_KEY = 'TEST_SECRET_KEY'

# TODO host will be different in kubernetes cluster
DATABASES = {
    'default': {
        'ENGINE': 'django_cockroachdb',
        'NAME': 'gitrello',
        'USER': 'gitrello',
        'PASSWORD': None,
        'HOST': '127.0.0.1',
        'PORT': '26257',
    }
}
