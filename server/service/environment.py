import os


class Environment:
    DATABASE_URL: str = None
    BOT_TOKEN: str = None
    CHAT_IDS: str = None


environmental_variables = Environment()


def get_env():
    environmental_variables.DATABASE_URL = os.environ.get("DATABASE_URL", None)
    environmental_variables.BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    environmental_variables.CHAT_IDS = os.environ.get("CHAT_IDS", None)

    if environmental_variables.DATABASE_URL is None or \
            environmental_variables.CHAT_IDS is None or \
            environmental_variables.BOT_TOKEN is None:
        raise Exception('MISSING ENVS! ABORTING!')


get_env()
