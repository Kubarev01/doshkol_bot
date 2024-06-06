from create_bot_doshkol import dp
from aiogram.utils import executor
import os

async def on_startup(_):
    print("Бот запущен")
    #здесь нужно подулючить бд
from handlers import client,admin

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)



executor.start_polling(dp,skip_updates=True,on_startup=on_startup)

