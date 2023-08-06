import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )


settings = Settings()
