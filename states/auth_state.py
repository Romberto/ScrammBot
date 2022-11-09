from aiogram.dispatcher.filters.state import State, StatesGroup


class AuthState(StatesGroup):
    nik = State()
    password = State()
