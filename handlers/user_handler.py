import os
from datetime import datetime

import aiohttp
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from googleapiclient.discovery import build

user_router = Router()

oauth_flow = {}


class Form(StatesGroup):
    waiting_for_auth = State()


def get_calendar_service(credentials):
    return build('calendar', 'v3', credentials=credentials)


@user_router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    oauth_url = os.getenv('OAUTH_SERVER_URL')
    auth_url = f"{oauth_url}/oauth/google/start?chat_id={message.chat.id}"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Authenticate with Google", url=auth_url)]
    ])
    await message.reply("Welcome! Please authenticate with Google Calendar to use this bot.", reply_markup=keyboard)


@user_router.message(Command("add_event"))
async def cmd_add_event(message: types.Message):
    if await check_auth(message.chat.id):
        # Implement add event logic here
        await message.reply("Adding an event... (implement this feature)")
    else:
        await request_authentication(message)


@user_router.message(Command("view_events"))
async def cmd_view_events(message: types.Message):
    if await check_auth(message.chat.id):
        events = await get_todays_events(message.chat.id)
        if events:
            response = "Today's events:\n\n"
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                start_time = datetime.fromisoformat(start).strftime('%H:%M')
                response += f"• {start_time} - {event['summary']}\n"
            await message.reply(response)
        else:
            await message.reply("You have no events scheduled for today.")
    else:
        await request_authentication(message)


async def get_todays_events(chat_id: int):
    async with aiohttp.ClientSession() as session:
        oauth_url = os.getenv('OAUTH_SERVER_URL')
        async with session.get(f"{oauth_url}/get_todays_events/{chat_id}") as resp:
            if resp.status == 200:
                data = await resp.json()
                return data['events']
            else:
                return None


async def request_authentication(message: types.Message):
    oauth_url = os.getenv('OAUTH_SERVER_URL')
    auth_url = f"{oauth_url}/oauth/google/start?chat_id={message.chat.id}"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Authenticate with Google", url=auth_url)]
    ])
    await message.reply("You need to authenticate first. Please click the button below:", reply_markup=keyboard)


async def check_auth(chat_id: int) -> bool:
    async with aiohttp.ClientSession() as session:
        oauth_url = os.getenv('OAUTH_SERVER_URL')
        async with session.get(f"{oauth_url}/check_auth/{chat_id}") as resp:
            auth_status = await resp.json()
    return auth_status.get('authenticated', False)
