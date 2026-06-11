import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import os

TOKEN = os.getenv("BOT_TOKEN")  # Токен будет храниться в секретах Render
# Убрали прокси – на сервере Render он не нужен

bot = Bot(token=TOKEN)
dp = Dispatcher()

# URL, где будет лежать index.html на Render (замените позже)
WEBAPP_URL = "https://ваш-сервис.onrender.com/index.html"

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Открыть игру", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer("Игра 'Кешбек-авантюрист'!", reply_markup=keyboard)

async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())