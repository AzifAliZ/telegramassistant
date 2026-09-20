import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL")
CONTACT_PHONE = os.getenv("CONTACT_PHONE")


if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing from .env")

if not CONTACT_EMAIL:
    raise ValueError("CONTACT_EMAIL is missing from .env")

if not CONTACT_PHONE:
    raise ValueError("CONTACT_PHONE is missing from .env")
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")

if not ADMIN_USER_ID:
    raise ValueError("ADMIN_USER_ID is missing from .env")

ADMIN_USER_ID = int(ADMIN_USER_ID)