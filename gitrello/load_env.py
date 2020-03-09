import os

from dotenv import load_dotenv


def load_env():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if (path := os.getenv('ENV_FILE')) is not None:
        load_dotenv(path)
        return
    elif os.path.exists(os.path.join(base_dir, '.env')):
        load_dotenv(os.path.join(base_dir, '.env'))
        return
    elif os.path.exists(os.path.join(base_dir, '.env.local')):
        load_dotenv(os.path.join(base_dir, '.env.local'))
        return

    raise IOError('.env file does not exist')
