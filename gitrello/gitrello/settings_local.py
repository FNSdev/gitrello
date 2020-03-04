from gitrello.settings import *


DEBUG = True

# To disable IPython debug messages
LOGGING['loggers']['parso'] = {
    'handlers': ['console_debug'],
    'level': 'INFO',
    'propagate': False,
}

ALLOWED_HOSTS = [
    '127.0.0.1',
]
