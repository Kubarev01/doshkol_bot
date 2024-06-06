import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram import types,Dispatcher
from create_bot_doshkol import dp,bot

from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardRemove,callback_query,ChatActions,ContentType
from aiogram.dispatcher.filters import Text, ContentTypeFilter



from aiogram import Bot
from aiogram.types import Message, LabeledPrice,PreCheckoutQuery,ShippingOption
from aiogram.types import ContentType
from aiogram.dispatcher.filters import ContentTypeFilter
from collections import deque


@dp.message_handler(commands=['r'])
async def check_working(message:types.Message):
    await bot.send_message(message.from_user.id,'Бот работает')

@dp.message_handler(commands=['start'])
async def startup(message:types.Message)->None:

    start_work=InlineKeyboardMarkup().add(InlineKeyboardButton("Приступить к работе",callback_data='start_bot'))
    await bot.send_message(message.from_user.id, f'Добро пожаловать в оффициальный телеграм-бот\n👦<b>дошколёнок67</b>👧',reply_markup=start_work,
                           parse_mode='html')



@dp.callback_query_handler(text='start_bot')
async def wellcome(callback_query:types.CallbackQuery):
    mess = 'График работы в учебное время.\n\n-----------------------------------------\n<b>ПН-ПТ</b> <i>16:00-20:00</i>\n<b>СБ</b> <i>10:00-16:00</i>\n<b>ВС</b> <i>ВЫХОДНОЙ</i>\n-----------------------------------------\n\nЗапись на новый учебный год осуществляется ежегодно с <b>01 июня</b>, по т.<i>63-13-44</i>, с 9.00-19.00 или в электронной форме на сайте/телеграмме.'
    visit_website = InlineKeyboardMarkup().add(
        InlineKeyboardButton('Перейти на сайт дошколёнок67.рф', url='http://дошколёнок67.рф/'))
    menu_kb=InlineKeyboardMarkup().add(InlineKeyboardButton("Записаться",callback_query='write_in'))

    await callback_query.message.answer(mess, reply_markup=visit_website, parse_mode='html')

    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=menu_kb)

def register_handlers_client(dp: Dispatcher):
    pass
    #dp.register_message_handler(startup,commands=['start'])
    #dp.register_message_handler(startup, Text(equals="привет", ignore_case=True))
