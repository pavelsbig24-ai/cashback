import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiohttp import web

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Адрес, где будет доступен index.html (тот же сервис Render)
WEBAPP_URL = "https://cashback-prd2.onrender.com/index.html"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ========== ОБРАБОТЧИКИ БОТА ==========
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Открыть игру", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer(
        "Добро пожаловать в 'Кешбек-авантюрист'!\n"
        "Покупай товары, получай кешбек, но не попадайся охране.",
        reply_markup=keyboard
    )

# ========== ВЕБ-СЕРВЕР ДЛЯ RENDER (чтобы не отключали) ==========
async def handle_health(request):
    return web.Response(text="OK")

async def run_web_server():
    app = web.Application()
    app.router.add_get("/", handle_health)
    app.router.add_get("/health", handle_health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("Веб-сервер для healthcheck запущен на порту 8080")

# ========== ЗАПУСК ==========
async def main():
    # Запускаем веб-сервер (чтобы Render видел порт)
    await run_web_server()
    # Запускаем бота
    print("Бот запущен и слушает команды...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
