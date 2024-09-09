import os


class Settings:
    MAX_NUMBER_OF_WORKERS = os.environ.get("MAX_NUMBER_OF_WORKERS")
