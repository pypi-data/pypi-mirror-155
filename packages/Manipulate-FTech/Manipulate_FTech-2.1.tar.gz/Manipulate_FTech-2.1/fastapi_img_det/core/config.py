import os

from dotenv import load_dotenv

load_dotenv("../.env")


ENVIRONMENT = os.environ.get("ENVIRONMENT")

