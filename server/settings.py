from pydantic import BaseSettings
from .main import users_db


class Settings(BaseSettings):
    app_name: str = "insta-scraper-with-fastAPI"
    admin_email: str = "amineyvazlou@gmail.com"
    default_posts: int = 100
    default_users: dict = {
        "amin": users_db["amin"],
        "sally": users_db["sally"],
    }
