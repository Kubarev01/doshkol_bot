from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton


admin_panel=InlineKeyboardMarkup()
a1=InlineKeyboardButton(text="Управление филлиалами",callback_data='admin_write_down')
a2=InlineKeyboardButton(text="🔧Настройки бота",callback_data='moderate_bot')
admin_panel.add(a1).add(a2)



schools=InlineKeyboardMarkup()
b1=InlineKeyboardButton(text='Лицей №1',callback_data='school_Лицей №1')
b2=InlineKeyboardButton(text='Школа №3',callback_data='school_Школа №3')
b3=InlineKeyboardButton(text='Школа №9',callback_data='school_Школа №9')
b4=InlineKeyboardButton(text='Школа №21',callback_data='school_Школа №21')
b5=InlineKeyboardButton(text='Школа №27',callback_data='school_Школа №27')
b6=InlineKeyboardButton(text='Школа №29',callback_data='school_Школа №29')
b7=InlineKeyboardButton(text='Школа №33',callback_data='school_Школа №33')
b8=InlineKeyboardButton(text='Школа №34',callback_data='school_Школа №34')
b9=InlineKeyboardButton(text='Школа №35',callback_data='school_Школа №35')
b10=InlineKeyboardButton(text='Школа №36',callback_data='school_Школа №36')
b11=InlineKeyboardButton(text='Соколовского 4',callback_data='school_Соколовского 4')
b12=InlineKeyboardButton(text='КЦ Заднепровье(Губенко 5)',callback_data='school_КЦ Заднепровье(Губенко)')
b13=InlineKeyboardButton(text='Печерская школа',callback_data='school_Печерская школа')
b14=InlineKeyboardButton(text='🔙Назад',callback_data='school_back')

schools.add(b1).insert(b2).add(b3).insert(b4).add(b5).insert(b6).add(b7).insert(b8).add(b9).insert(b10).add(b11).insert(b12).add(b13).add(b14)


moderate_bot_kb=InlineKeyboardMarkup()
m1=InlineKeyboardButton(text='Выгрузить отчет в xl-файле',callback_data='moderate_bot_loadxl')
m2=InlineKeyboardButton(text='Назад',callback_data='moderate_bot_back')
moderate_bot_kb.add(m1).add(m2)

time_and_days=InlineKeyboardMarkup()
c1=InlineKeyboardButton(text="ПН/ЧТ 17:00",callback_data="date_ПН/ЧТ 17:00")
c2=InlineKeyboardButton(text="ПН/ЧТ 18:00",callback_data="date_ПН/ЧТ 18:00")
c3=InlineKeyboardButton(text="ПН/ЧТ 19:00",callback_data="date_ПН/ЧТ 19:00")

c4=InlineKeyboardButton(text="ВТ/ПТ 17:00",callback_data="date_ВТ/ПТ 17:00")
c5=InlineKeyboardButton(text="ВТ/ПТ 18:00",callback_data="date_ВТ/ПТ 18:00")
c6=InlineKeyboardButton(text="ВТ/ПТ 19:00",callback_data="date_ВТ/ПТ 19:00")

c7=InlineKeyboardButton(text='🔙Назад',callback_data='date_back')

time_and_days.add(c1).insert(c2).insert(c3).add(c4).insert(c5).insert(c6).add(c7)



back_kb=InlineKeyboardMarkup()
h1=InlineKeyboardButton(text='🔙Вернуться назад',callback_data='adreb_back')
back_kb.add(h1)


is_right=InlineKeyboardMarkup()
i1=InlineKeyboardButton(text='✅',callback_data='is_right_yes')
i2=InlineKeyboardButton(text='❌',callback_data='is_right_no')
is_right.add(i1).insert(i2)


async def get_groups(childs):
    child_groups = InlineKeyboardMarkup()
    print(childs)
    names = []
    ids = []

    for index, value in enumerate(childs):
        if index % 2 == 0:  # проверяем четный ли индекс
            ids.append(value)
        else:
            names.append(value)

    for child in childs:


        r = InlineKeyboardButton(text='🧒'+child, callback_data=f'child_{child}')
        child_groups.add(r)
    child_groups.add(InlineKeyboardButton(text=f'➕ДОБАВИТЬ В ГРУППУ',callback_data='child_add')).add(InlineKeyboardButton(text='🔙Назад',callback_data='child_back'))

    return child_groups


kb_for_edit_child=InlineKeyboardMarkup()
t1=InlineKeyboardButton(text='Изменить данные',callback_data='edit_child_edit')
t2=InlineKeyboardButton(text='Удалить навсегда',callback_data='edit_child_delete')
t3=InlineKeyboardButton(text='Назад',callback_data='edit_child_back')
kb_for_edit_child.add(t1).add(t2).add(t3)

edit_kb=InlineKeyboardMarkup()
v1=InlineKeyboardButton(text='ФИО ребёнка',callback_data='rewrite_fio')
v2=InlineKeyboardButton(text='Филиал',callback_data='rewrite_school')
v3=InlineKeyboardButton(text='Время',callback_data='rewrite_time')
v4=InlineKeyboardButton(text='ФИО родителей',callback_data='rewrite_fioparents')
v5=InlineKeyboardButton(text='Номер телефона',callback_data='rewrite_number')
v6=InlineKeyboardButton(text='Вернуться назад',callback_data='rewrite_back')
edit_kb.add(v1).insert(v2).insert(v3).add(v4).insert(v5).add(v6)





