# server.py
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.filters import Command
import asyncio

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
print("BOT_TOKEN:", BOT_TOKEN)

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN .env faylda topilmadi!")

# botni yaratish
bot = Bot(token=BOT_TOKEN)

# Dispatcher bot bilan ulanadi
dp = Dispatcher()

# Aiogram 3.4.1 da start_polling ga bot berish kerak
async def main():
    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

WEBAPP_URL = "https://www.pythonanywhere.com/user/muzafxxs/files/home/muzafxxs/mysite/miniapp/index.html"

@dp.message(Command(commands=["start"]))
async def start_cmd(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Mini Appni ochish", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer("Salom! Pastdagi tugmadan Mini Appni oching 👇", reply_markup=kb)

if __name__ == "__main__":
    asyncio.run(main())
