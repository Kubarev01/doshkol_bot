import asyncio


from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram import types,Dispatcher


from create_bot_doshkol import dp,bot
from keyboards.admin_keyboard import kb_agrement
from keyboards.admin_Inline_kb import admin_panel,schools,time_and_days,get_groups,back_kb,is_right,kb_for_edit_child,edit_kb,moderate_bot_kb
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardRemove,callback_query,ChatActions,ContentType
from aiogram.dispatcher.filters import Text, ContentTypeFilter
from data_storage import excel_behav
from collections import deque


moderator_ID=None
message_stack=deque()

class FSMAdmin(StatesGroup):
    moderate_bot=State()
    moderate_bot_exl_path=State()
    write_a_child=State()
    school=State()
    date_and_time=State()
    obrabot_group=State()
    add_child=State()
    add_child1=State()
    add_child2=State()
    add_child3=State()
    agrement=State()
    finish_add_child=State()
    confirm_add_child=State()
    ready_to_edit=State()
    ready_to_edit_1=State()
    edit_data=State()
    rewrite_data=State()
    get_new_data_from_admin=State()

@dp.message_handler(commands=['activate'])
async def admin_check(message:types.Message):
    global moderator_ID
    moderator_ID = message.from_user.id
    await message.delete()


@dp.message_handler(commands=['admin'])
async def show_admin_panel(message:types.Message):
    if message.from_user.id==moderator_ID:
        message_stack.clear()
        await bot.send_message(message.from_user.id,"👩‍💼Панель администратора",reply_markup=admin_panel,parse_mode='html')
        await FSMAdmin.write_a_child.set()

@dp.callback_query_handler(text='moderate_bot',state='*')
async def moderate_bot(callback_query:types.CallbackQuery,state: FSMContext):
    if callback_query.message.chat.id == moderator_ID:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,message_id=callback_query.message.message_id,text="Выберите пункт меню",reply_markup=moderate_bot_kb)

@dp.callback_query_handler(text='moderate_bot_loadxl',state='*')
async def point_xl_path(callback_query:types.CallbackQuery,state: FSMContext):
    if callback_query.message.chat.id == moderator_ID:
        temp_file=await excel_behav.save_xl_file()
        with open(temp_file.name, 'rb') as file:

            document = types.InputFile(file)

            mess= await bot.send_document(chat_id=callback_query.message.chat.id,document=document)

        temp_file.close()
        message_stack.append(mess)
        #await bot.send_message(callback_query.message.chat.id,f'Для возращения в главное меню нажмите на кнопку:')

#     if message.from_user.id==moderator_ID:
#         await excel_behav.change_path(message.text)
#         await bot.answer_callback_query(message.message_id, text='ПУТЬ К EXEL ФАЙЛУ ИЗМЕНЕН', show_alert=True)
#
@dp.callback_query_handler(text='moderate_bot_back',state='*')
async def cancel(callback_query:types.CallbackQuery,state:FSMContext):
    if callback_query.message.chat.id == moderator_ID:

        await state.finish()
        
        if len(message_stack)==1:
            print('больше или равно 2')
            await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id+1)
            await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id )
        if len(message_stack)<1:
            await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        await show_admin_panel(message=callback_query)


# @dp.message_handler(commands=['menu'],state='*')
# async def cancel(message:types.Message,state:FSMContext):
#     if message.from_user.id == moderator_ID:
#         await bot.delete_message(message.chat.id,message.message_id-3)
#         await bot.delete_message(message.chat.id,message.message_id-2)
#         await bot.delete_message(message.chat.id,message.message_id-1)
#         await bot.delete_message(message.chat.id, message.message_id)
#         await state.finish()
#         await show_admin_panel(message)


@dp.callback_query_handler(text='admin_write_down',state=FSMAdmin.write_a_child)
async def start_to_add_child(callback_query:types.CallbackQuery,state:FSMContext):
    if callback_query.message.chat.id == moderator_ID:
        #await bot.send_message(callback_query.message.from_user.id,"добавить:")
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,message_id=callback_query.message.message_id,text="🏫Выберите филиал",reply_markup=schools,parse_mode='html')
        await FSMAdmin.school.set()


@dp.callback_query_handler(Text(startswith='school_'),state=FSMAdmin.school)
async def obrabot_school(callback_query:types.CallbackQuery,state:FSMContext):
    if callback_query.message.chat.id==moderator_ID:
        res=callback_query.data
        if res=='school_back':
            await show_admin_panel(callback_query.message)
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,message_id=callback_query.message.message_id ,text="👩‍💼Панель администратора", reply_markup=admin_panel,
                               parse_mode='html')
            await FSMAdmin.write_a_child.set()
            return
        else:
            if callback_query.data != 'child_back':

                async with state.proxy() as data:
                    data['school']=callback_query.data.split('_')[1]


            await bot.edit_message_text(chat_id=callback_query.message.chat.id,message_id=callback_query.message.message_id,text=f"🏫{data['school']}\n 📆Выберите время и дни", reply_markup=time_and_days)
            await FSMAdmin.date_and_time.set()


@dp.callback_query_handler(Text(startswith='date_'),state=FSMAdmin.date_and_time)
async def add_date_and_time(callback_query:types.CallbackQuery,state:FSMContext):

    if callback_query.message.chat.id==moderator_ID:

        if callback_query.data=="date_back":

            await FSMAdmin.school.set()
            await start_to_add_child(callback_query,state)
            # await bot.edit_message_text(chat_id=callback_query.message.chat.id,
            #                             message_id=callback_query.message.message_id, text="🏫Выберите филиал",
            #                             reply_markup=schools, parse_mode='html')

            return

        else:
            if callback_query.data.startswith('date_'):
                async with state.proxy() as data:
                    data['time']=callback_query.data.split('_')[1]
                    school=data['school']
                    time=data['time']
            else:
                async with state.proxy() as data:
                    school=data['school']
                    time=data['time']

            #здесь должен получаться список детей из группы

            lst=await excel_behav.read_child(school,time)


            await FSMAdmin.obrabot_group.set()

            async with state.proxy() as data:
                message_text = f"🏫<b>Филиал</b>: {data['school']}\n" \
                               f"🕒<b>Время</b>: {data['time']}\n" \
                               f"👥<b>Детей в группе</b>: {len(lst)}/6\n\n" \
                               f"ДЛЯ УПРАВЛЕНИЯ РЕБЁНКОМ И ПРОСМОТРОМ ИНФОРМАЦИИ НАЖМИТЕ НА НЕГО\n\n" \
                               f"🔴-<i>не подписанные договоры</i>"\

            if len(message_stack)>=1:
                print("стак сработал")
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id-1,
                    text=message_text,
                    reply_markup=await(get_groups(lst)),
                    parse_mode='html'
                )
                message_stack.clear()
            else:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text=message_text,
                    reply_markup=await(get_groups(lst)),
                    parse_mode='html'
                )
            # async with state.proxy() as data:
            #         await bot.edit_message_text(chat_id=callback_query.message.chat.id,message_id=callback_query.message.message_id,text=f"🏫<b>Филиал</b>: {data['school']}\n"
            #                                                           f"🕒<b>Время</b>: {data['time']}\n👥<b>Детей в группе</b>: {len(lst)}/6\n\n"
            #                                                           f"ДЛЯ УПРАВЛЕНИЯ РЕБЁНКОМ И ПРОСМОТРОМ ИНФОРМАЦИИ НАЖМИТЕ НА НЕГО",reply_markup=await(get_groups(lst)),parse_mode='html')
            # # except:
            #     #await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)
            #     async with state.proxy() as data:
            #         await bot.edit_message_text(chat_id=callback_query.message.chat.id,
            #                                     message_id=callback_query.message.message_id-1,
            #                                     text=f"🏫<b>Филиал</b>: {data['school']}\n"
            #                                          f"🕒<b>Время</b>: {data['time']}\n👥<b>Детей в группе</b>: {len(lst)}/6\n\n"
            #                                          f"ДЛЯ УПРАВЛЕНИЯ РЕБЁНКОМ И ПРОСМОТРОМ ИНФОРМАЦИИ НАЖМИТЕ НА НЕГО",
            #                                     reply_markup=await(get_groups(lst)), parse_mode='html')


            print("1")








@dp.callback_query_handler(Text(startswith='child_'),state="*")
async def obrabot_group(callback_query:types.CallbackQuery,state:FSMContext):
    print("2")
    if callback_query.message.chat.id == moderator_ID:
        if callback_query.data=='child_back':
            await bot.answer_callback_query(callback_query.id,
                                            text='Введите данные о филиале заново ', show_alert=True)
            await FSMAdmin.write_a_child.set()
            await start_to_add_child(callback_query,state)
            return

        if callback_query.data.split('_')[1]=='add':
            await FSMAdmin.add_child.set()
            await add_child(callback_query,state)
            return

        else:
            if 'child_' not in callback_query.data:
                async with state.proxy() as data:
                    child_dict=data['child_dict']
                    #print("значение словарая если _child не в калбекдата"+child_dict)
            if 'child_' in callback_query.data:
                async with state.proxy() as data:
                    print('вход '+callback_query.data.split('_')[1])
                    child_dict=await excel_behav.info_child(child=callback_query.data.split('_')[1])
                    print(child_dict)
                    data['child_dict']=child_dict

                    print(child_dict)
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text=f'ВЫ В РЕЖИМЕ РЕДАКТИРОВАНИЯ ИНФОРМАЦИИ О РЕБЁНКЕ\n\n🧒<b>ФИО</b>: {child_dict["fio"]}\n🏫<b>Филлиал</b>: {child_dict["school"]}\n🕒<b>Время</b>: {child_dict["time"]}\n👨‍💼<b>ФИО родителей</b>: {child_dict["fioparents"]}\n📞<b>Контактный телефон</b>: {child_dict["number"]}\n<b>📃Статус договора</b>: {child_dict["agrement"]}',
                                        reply_markup=kb_for_edit_child,
                                        parse_mode='html')

            await FSMAdmin.edit_data.set()
            await edit_data(callback_query,state)


@dp.message_handler(state=FSMAdmin.ready_to_edit)
async def fill_new_data(message:types.Message,state:FSMContext):
    if message.chat.id==moderator_ID:
        async with state.proxy() as data:
            print("принятие новых данныых"+message.text)
            data['param']=message.text
            await excel_behav.fill_new_param(message,state)
            print("tes 1")
            #await bot.delete_message(message.chat.id,message.message_id)
            callback_query = types.CallbackQuery(message=message)
            callback_query.data='data_1'
            print('tes 2')
            #await bot.answer_callback_query(callback_query.id,'Изменения внесены',show_alert=True)
            await bot.delete_message(message.from_user.id, message.message_id)
            message_stack.append(1)
            await FSMAdmin.date_and_time.set()
            await add_date_and_time(callback_query,state)

            print('tes 3')

@dp.callback_query_handler(state=FSMAdmin.ready_to_edit_1)
async def fill_new_data_1(callback_query:types.CallbackQuery,state:FSMContext):
    if callback_query.message.chat.id==moderator_ID:
        async with state.proxy() as data:
            print("принятие новых данныых")

            data['param']=callback_query.data
            print(data['param'])
            await excel_behav.fill_new_param1(callback_query,state)
            print("tes 1")
            #await bot.delete_message(message.chat.id,message.message_id)

            print('tes 2')

            #await bot.answer_callback_query(callback_query.id,'Изменения внесены',show_alert=True)
            await FSMAdmin.date_and_time.set()
            await add_date_and_time(callback_query,state)
            await bot.delete_message(callback_query.message.from_user.id,callback_query.message.message_id)
            print('tes 3')

@dp.callback_query_handler(Text(startswith='rewrite_'),state=FSMAdmin.rewrite_data)
async def rewrite_data(callback_query:types.CallbackQuery,state:FSMContext):
    if callback_query.message.chat.id==moderator_ID:
        async with state.proxy() as data:
            print("хендлер перезаписи")
            child_dict=data['child_dict']

            await excel_behav.edit_param(callback_query,child_dict=child_dict,param=callback_query.data.split('_')[1],state=state)
            end_param=await excel_behav.edit_in_xl(callback_query,state)
            if end_param =='back':
                await add_date_and_time(callback_query, state)
            #await excel_behav.fill_new_param(callback_query.message,state)


            print(131242352)
            print(end_param)
            #await add_date_and_time(callback_query,state)
            if end_param in ['school','time','number','agrement']:
                await FSMAdmin.ready_to_edit_1.set()
            else:
                await FSMAdmin.ready_to_edit.set()

        if callback_query.data=='rewrite_back':
            await obrabot_group(callback_query,state)
            return




@dp.callback_query_handler(Text(startswith='edit_child'),state=FSMAdmin.edit_data)
async def edit_data(callback_query:types.CallbackQuery,state:FSMContext):
    if callback_query.message.chat.id==moderator_ID:
        if callback_query.data=='edit_child_edit':
            async with state.proxy() as data:
                child_dict=data['child_dict']
                await bot.edit_message_text(chat_id=callback_query.message.chat.id,message_id=callback_query.message.message_id,text=f'Что нужно изменить?\n🧒<b>ФИО</b>: {child_dict["fio"]}\n🏫<b>Филлиал</b>: {child_dict["school"]}\n🕒<b>Время</b>: {child_dict["time"]}\n👨‍💼<b>ФИО родителей</b>: {child_dict["fioparents"]}\n📞<b>Контактный телефон</b>: {child_dict["number"]}\n<b>📃Статус договора</b>: {child_dict["agrement"]}',reply_markup=edit_kb,parse_mode='html')
                await FSMAdmin.rewrite_data.set()
                return

        if callback_query.data=='edit_child_delete':
            async with state.proxy() as data:
                child_dict=data['child_dict']
                print(child_dict)
                await excel_behav.delete_from_xl(child_dict)
                await FSMAdmin.date_and_time.set()
                await add_date_and_time(callback_query,state)
                return
        if callback_query.data=='edit_child_back':
            await FSMAdmin.date_and_time.set()
            await add_date_and_time(callback_query, state)
            return



@dp.callback_query_handler(state=FSMAdmin.add_child)
async def add_child(callback_query:types.CallbackQuery,state:FSMContext):
    if callback_query.message.chat.id == moderator_ID:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        await bot.send_message(callback_query.message.chat.id,'Введите ФИО ребёнка')
        await FSMAdmin.add_child1.set()



@dp.message_handler(state=FSMAdmin.add_child1)
async def add_child1(message:types.Message,state:FSMContext):
    print('3')
    if message.from_user.id == moderator_ID:
        # if callback_query.data=='adreb_back':
        #     await add_date_and_time(callback_query,state)
        #     await FSMAdmin.date_and_time.set()
        #
        #     return

        async with state.proxy() as data:
            data['fio']=message.text
        await message.answer("Теперь введите ФИО родителей")
        await FSMAdmin.add_child2.set()

@dp.message_handler(state=FSMAdmin.add_child2)
async def add_child2(message: types.Message, state: FSMContext):
    print('4')
    if message.from_user.id == moderator_ID:
        # if callback_query.data=='adreb_back':
        #     await add_date_and_time(callback_query,state)
        #     await FSMAdmin.date_and_time.set()
        #
        #     return

        async with state.proxy() as data:
            data['fioparents'] = message.text

        await message.answer("Теперь введите номер телефона родителей")
        await FSMAdmin.add_child3.set()



@dp.message_handler(state=FSMAdmin.add_child3)
async def add_child3(message: types.Message, state: FSMContext):
    print('5')
    if message.from_user.id == moderator_ID:
        # if callback_query.data=='adreb_back':
        #     await add_date_and_time(callback_query,state)
        #     await FSMAdmin.date_and_time.set()
        #
        #     return

        if not len(message.text) == 12 and not message.text.startswith("+7"):
            await bot.send_message(message.chat.id,
                                   'Неправильный формат номера. Введите ваш номер телефона в формате +7**********.')
            return

        async with state.proxy() as data:
            data['number'] = message.text
        await message.answer("Укажите статус договора",reply_markup=kb_agrement)
        await FSMAdmin.agrement.set()





@dp.message_handler(state=FSMAdmin.agrement)
async def agrement_add(message:types.Message,state:FSMContext):
    if message.from_user.id==moderator_ID:


        async with state.proxy() as data:
            if message.text =='✅Договор подписан':
                data['agrement']='подписан'
            if message.text == '❌Договор не подписан':
                data['agrement']='не подписан'



            await bot.send_message(message.from_user.id,
                               f"🏫{data['school']}\n🕒{data['time']}\n🧒{data['fio']}\n👨‍💼{data['fioparents']}\n📞{data['number']}\n📃{data['agrement']}",
                               reply_markup=is_right)

        await FSMAdmin.confirm_add_child.set()
        print('finish')

@dp.callback_query_handler(Text(startswith='is_right_'),state=FSMAdmin.confirm_add_child)
async def confirm_add_child(callback_query:types.CallbackQuery,state:FSMContext):
    if callback_query.message.chat.id == moderator_ID:
        print('adding_child to xl')
        ans=callback_query.data.split('_')[2]
        if ans=='yes':
            #добавление в xl
            await bot.answer_callback_query(callback_query.id, text='Ребёнок успешно добавлен в группу!', show_alert=True)
            await excel_behav.insert_child(state)
            await add_date_and_time(callback_query, state)
            await FSMAdmin.date_and_time.set()
            return
        if ans=='no':
            await bot.answer_callback_query(callback_query.id,text='Возврат к редактированию группы',show_alert=True)
            async with state.proxy() as data:
                del data['fio']
                del data['fioparents']
                del data['number']
                del data['agrement']

            await add_date_and_time(callback_query, state)
            await FSMAdmin.date_and_time.set()
            return

# @dp.message_handler(state=FSMAdmin.finish_add_child)
# async def add_child4(message: types.Message, state: FSMContext):
#     print('yo')
#     if message.from_user.id == moderator_ID:
#         async with state.proxy() as data:
#             await bot.send_message(message.from_user.id,f"🏫{data['school']}\n🕒{data['time']}\n🧒{data['fio']}\n👨‍💼{data['fioparents']}\n📞{data['number']}")





# @dp.callback_query_handler(state=FSMAdmin.add_child11)
# async def add_child11(message:types.Message,state:FSMContext):
#     if callback_query.message.chat.id==moderator_ID:
#         if callback_query.data=='adreb_back':
#             await add_date_and_time(callback_query,state)
#             await FSMAdmin.date_and_time.set()
#             return
#
#         async with state.proxy() as data:
#             data['child_name']=message.from_user.text
#             print(data['child_name'])
#





def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_check, Text(equals="админ", ignore_case=True), is_chat_admin=True)