import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.filters import Command
import asyncio
from aiohttp import web

# .env fayldan sozlamalarni yuklash
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")  # server URL + miniapp path
PORT = int(os.getenv("PORT", 8000))  # default 8000

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN .env faylda topilmadi!")

# Logging
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher yaratish
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Telegram bot start komandasi
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🚀 Mini Appni ochish",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    await message.answer("Salom! Pastdagi tugmadan Mini Appni oching 👇", reply_markup=kb)

# Web server uchun handler
async def handle_miniapp(request):
    return web.Response(text="Mini App sahifasi ishlamoqda!", content_type='text/html')

# Aiohttp web server yaratish
async def init_app():
    app = web.Application()
    app.add_routes([web.get('/miniapp', handle_miniapp)])
    return app

# Bot va web serverni birga ishga tushirish
async def main():
    runner = web.AppRunner(await init_app())
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    logging.info(f"Web server ishga tushdi: http://0.0.0.0:{PORT}")

    logging.info("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
