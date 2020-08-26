from pathlib import Path

from dotenv import load_dotenv

env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

from gitrello.settings import *

SECRET_KEY = 'aDFgbU43GTgf@34cxbJhg7gsgd^hdgH%'

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
