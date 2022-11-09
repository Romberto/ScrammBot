from aiogram import types, Dispatcher
from database.config_db import get_user_db, set_secret_key, add_user, get_auth_user
from manager.random_cod import generate_random_cod
from aiogram.dispatcher import FSMContext
from states import AuthState
from config import EMPLOUEES_LIST


# @dp.message_handler(commands=['start'])
async def echo(message: types.Message):
    auth = await get_auth_user()
    if not str(message.chat.id) in auth:
        await AuthState.nik.set()
        await message.answer('Добрый день, для синхронизации с CRM свой nik_name')
    else:
        await message.answer('вы зарегистрированны')


# ловим nic_name
async def echo_pass(message: types.Message, state=FSMContext):
    nik_name = message.text
    user = await get_user_db(nik_name)
    if user:
        await state.update_data(nik=nik_name, user_id=user[0])
        await AuthState.next()
        random_cod = await generate_random_cod()  # генерируем секретный код
        await state.update_data(cod=random_cod)
        await set_secret_key(user[0], random_cod)
        await message.answer(
            "Перейдите в CRM в личном кабинете вы найдёте секретный код, отправте его в ответ на это сообщение")
    else:
        await message.answer('С таким nik_name пользователей не обнаруженоо')
        await message.answer('Для синхронизации с CRM свой nik_name')


async def echo_finish(message: types.Message, state=FSMContext):
    password = message.text
    state_data = await state.get_data()
    if password == str(state_data['cod']):
        await set_secret_key(state_data['user_id'], None)
        await add_user(state_data['user_id'], message.chat.id)
        await message.answer("Поздравляем сопряжение удалось перезагрузите страницу 'Личный кабнет'")
        await state.finish()
    else:
        await message.answer("что-то пошло не так")

    await state.update_data(password=message.text)


def register_handlers_auth(dp: Dispatcher):
    dp.register_message_handler(echo, commands=['start'])
    dp.register_message_handler(echo_pass, state=AuthState.nik, content_types=['text'])
    dp.register_message_handler(echo_finish, state=AuthState.password, content_types=['text'])
