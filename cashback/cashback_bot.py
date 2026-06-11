import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = "https://cashback-prd2.onrender.com/index.html"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Открыть игру", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer("Добро пожаловать в 'Кешбек-авантюрист'!", reply_markup=keyboard)

# ---- Раздача статических файлов (картинки, html) ----
async def handle_index(request):
    return web.FileResponse('index.html')

async def handle_static(request):
    filename = request.match_info['filename']
    # Проверяем, существует ли файл
    if os.path.exists(filename):
        return web.FileResponse(filename)
    else:
        return web.Response(status=404, text="File not found")

async def run_web_server():
    app = web.Application()
    app.router.add_get('/', handle_index)
    app.router.add_get('/index.html', handle_index)
    app.router.add_get('/{filename}', handle_static)  # ловит любые файлы (jpg, png, html)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("Веб-сервер запущен на порту 8080, отдаёт статику")
# ----------------------------------------------------

async def main():
    await run_web_server()
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
