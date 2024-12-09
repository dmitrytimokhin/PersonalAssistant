import os
import logging
from typing import Union

from aiogram import F, Router
from aiogram.filters import CommandStart, Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
from keyboards import kb_main

base_router = Router()
logger = logging.getLogger('MAIN')
load_dotenv()


# --- Старт телеграм бота ---
@base_router.message(or_f(CommandStart(), F.text == '/start'))
async def cmd_start(message: Message, state: FSMContext):
    tg_user_id = message.from_user.id
    await state.clear()
    logger.debug(msg=f'The User {tg_user_id} pressed start')
    await message.answer(
        text='Добро пожаловать! Вас приветствует ваш личный AI ассистент!'
             '\n\nОбщение со мной происходит посредством клавиатуры, кнопок и команд! \U00002B07'
             '\n\nА теперь приступим к работе \U0001F60A',
        reply_markup=kb_main)


@base_router.message(Command('update'))
async def cmd_update(message: Message, state: FSMContext):
    tg_user_id = message.from_user.id
    await state.clear()
    logger.debug(msg=f'The User {tg_user_id} pressed update')
    logger.debug(msg=f'The User {tg_user_id} pressed start')
    await message.answer(text=f'Спасибо! Бот обновлен до версии {os.getenv("VERSION")}'
                              '\n\nОбщение со мной происходит посредством клавиатуры, кнопок и команд! \U00002B07'
                              '\n\nА теперь приступим к работе \U0001F60A',
                         reply_markup=kb_main)


@base_router.message(Command('id'))
async def cmd_id(message: Message, state: FSMContext):
    tg_user_id = message.from_user.id
    tg_chat_id = message.chat.id
    await state.clear()
    logger.debug(msg=f'The User {tg_user_id} pressed get_id')
    if tg_user_id == tg_chat_id:
        await message.reply(text=f'Ваш уникальный номер: {tg_user_id}')
    else:
        await message.reply(text=f'Ваш уникальный номер: {tg_user_id},'
                                 f'\nУникальный номер чата: {tg_chat_id}')


# --- Handler на главное меню ---
@base_router.message(F.text.in_({'На главное меню', '/cancel'}))
async def go_home(message: Message, state: FSMContext):
    tg_user_id = message.from_user.id
    await state.clear()
    logger.debug(msg=f'The User {tg_user_id} pressed /cancel')
    await message.reply(text='Вы вернулись на главное меню!'
                             '\n\nПожалуйста, выберите пункт в меню на <b>клавиатуре</b> \U00002B07',
                        reply_markup=kb_main)


# --- Callback на главное меню ---
@base_router.callback_query(F.data == 'go_home')
async def go_home(callback: CallbackQuery, state: FSMContext):
    tg_user_id = callback.from_user.id
    await state.clear()
    logger.debug(msg=f'The User {tg_user_id} pressed /go_home')
    await callback.answer(text='Вы нажали "На главную"')
    await callback.message.reply(text='Вы вернулись на главное меню!'
                                      '\n\nПожалуйста, выберите пункт в меню на <b>клавиатуре</b> \U00002B07',
                                 reply_markup=kb_main)


#@base_router.message()
#async def un_know(message: Message, state: FSMContext):
#    await state.clear()
#    await message.answer(text='Я вас не понимаю \U0001F614'
#                              '\n\nОбщение со мной происходит посредством <b>клавиатуры, кнопок и '
#                              'команд</b> \U00002B07',
#                         reply_markup=kb_main)


#@base_router.callback_query()
#async def un_know(callback: CallbackQuery, state: FSMContext):
#    await state.clear()
#    await callback.answer(text='Вы нажимали "На главную"'
#                               '\n\nПожалуйста, начните с главного меню \U00002B07',
#                          show_alert=True)
