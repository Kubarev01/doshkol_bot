from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

b1=KeyboardButton(text='✅Договор подписан')
b2=KeyboardButton(text='❌Договор не подписан')

kb_agrement=ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
kb_agrement.add(b1).insert(b2)