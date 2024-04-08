import os


class Environment:
    DATABASE_URL: str = None


env = Environment()


def get_env():
    env.DATABASE_URL = os.environ.get("DATABASE_URL", None)


get_env()
