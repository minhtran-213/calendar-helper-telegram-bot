from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import os

load_dotenv()

default_config = DefaultBotProperties(parse_mode="HTML")

bot = Bot(token=os.getenv("TELE_TOKEN"),
          default=default_config)


