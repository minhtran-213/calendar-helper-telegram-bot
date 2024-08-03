from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import os

load_dotenv()

default_config = DefaultBotProperties(parse_mode="HTML")

bot = Bot(token=os.getenv("TELE_TOKEN"),
          default=default_config)

google_client_config = {"web": {"client_id": "155903417554-pal935o460shm487gl4uli6d8rmdaehm.apps.googleusercontent.com",
                                "project_id": "",
                                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                                "token_uri": "https://oauth2.googleapis.com/token",
                                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                                "client_secret": "secret",
                                "redirect_uris": ["https://t.me/NexusTaskBot?start=auth_{CODE}"]}}
