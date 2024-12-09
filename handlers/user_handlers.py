import logging
import os.path
import subprocess
from gpt4all import GPT4All
import threading
from aiogtrans import Translator
import speech_recognition as sr

import asyncio
from aiogram import F, Router
from aiogram.types import Message
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from handlers import FSMg4f, FSMs2t
from keyboards import kb_reply_go_home

user_router = Router()
logger = logging.getLogger('MAIN')

CONVERSATION_HISTORY = {}
TRANSLATOR = Translator()
MODEL = GPT4All("orca-mini-3b-gguf2-q4_0.gguf", device='cpu')

S2T = sr.Recognizer()


async def gen_response(prompt: str) -> str:
    with MODEL.chat_session():
        prompt_en = (await TRANSLATOR.translate(prompt, dest='en')).text
        answer = MODEL.generate(prompt_en,
                                max_tokens=200,
                                temp=0.7,
                                top_k=40,
                                top_p=0.4,
                                repeat_penalty=1.18,
                                repeat_last_n=64,
                                n_batch=8,
                                n_predict=None,
                                streaming=False)
        answer = (await TRANSLATOR.translate(answer, dest='ru')).text
    return answer


# --- GPT ---
@user_router.message(F.text == 'Воспользоваться GPT')
async def question_gpt(message: Message, state: FSMContext):
    tg_user_id = message.from_user.id
    logger.debug(msg=f'The User {tg_user_id} pressed "Воспользоваться GPT"')
    await state.clear()
    await state.set_state(FSMg4f.tg_user_id)
    await state.update_data(tg_user_id=tg_user_id)
    await state.set_state(FSMg4f.user_context)
    await message.reply(text='Введите ваш запрос',
                        reply_markup=kb_reply_go_home)


@user_router.message(FSMg4f.user_context)
async def answer_s2t(message: Message, state: FSMContext):
    tg_user_id = message.from_user.id
    logger.debug(msg=f'The User {tg_user_id} send request for gpt')
    prompt = message.text
    await state.update_data(user_context=prompt)
    await state.set_state(FSMg4f.process)
    answer = await gen_response(prompt=prompt)
    await message.reply(text=f'{answer}',
                        reply_markup=kb_reply_go_home)


# --- S2T ---
@user_router.message(F.text == 'Воспользоваться s2t')
async def question_s2t(message: Message, state: FSMContext):
    tg_user_id = message.from_user.id
    logger.debug(msg=f'The User {tg_user_id} pressed "Воспользоваться s2t"')
    await state.clear()
    await state.set_state(FSMs2t.tg_user_id)
    await state.update_data(tg_user_id=tg_user_id)
    await state.set_state(FSMs2t.audio)
    await message.reply(text='Отправьте мне аудио для транскрибации',
                        reply_markup=kb_reply_go_home)


@user_router.message(F.audio, FSMs2t.audio)
async def answer_s2t(message: Message, state: FSMContext):
    tg_user_id = message.from_user.id
    logger.debug(msg=f'The User {tg_user_id} send FSMs2t.audio')
    split_tup = os.path.splitext(message.audio.file_name)
    file_name = f'{split_tup[0]}_{message.from_user.full_name}{split_tup[1]}'
    await message.bot.download(file=message.audio.file_id,
                               destination=f'{file_name}')

    file_name_wav = f'{split_tup[0]}_{message.from_user.full_name}.wav'
    subprocess.call(['ffmpeg', '-i', file_name, file_name_wav])

    with sr.AudioFile(file_name_wav) as source:
        audio = S2T.record(source)
    answer_text = S2T.recognize_google_cloud(audio, language='ru')
    await message.answer(text=answer_text,
                         reply_markup=kb_reply_go_home)
    await state.clear()
    os.remove(file_name)
    os.remove(file_name_wav)
