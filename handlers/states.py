from aiogram.fsm.state import StatesGroup, State


class FSMg4f(StatesGroup):
    tg_user_id = State()
    user_context = State()
    process = State()


class FSMs2t(StatesGroup):
    tg_user_id = State()
    audio = State()
    process = State()
