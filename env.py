import os
from dotenv import load_dotenv
from typing import Optional


class Env:
    def __init__(self):
        load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

    def get(self, key: str) -> Optional[str]:
        return os.environ.get(key)


env = Env()
