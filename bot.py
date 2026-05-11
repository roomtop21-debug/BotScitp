import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web

# Получаем токен из переменных окружения
TOKEN = os.getenv("8643887906:AAFpXr1Ewc4vCYmlh2QqCr1MbKtpVvV0Oic")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Я работаю 24/7.")

# Мини-сервер для Render, чтобы он не засыпал
async def handle(request):
    return web.Response(text="Bot is alive")

async def main():
    # Запуск веб-сервера на порту, который даст Render
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    
    # Запускаем сервер фоном
    asyncio.create_task(site.start())
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
