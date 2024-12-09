from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

kb_main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Воспользоваться GPT')],
                                        [KeyboardButton(text='Воспользоваться s2t')],
                                        [KeyboardButton(text='Инструкция о системе')]],
                              resize_keyboard=True,
                              one_time_keyboard=True,
                              input_field_placeholder='Выберите пункт...')

kb_confirm = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Да',
                                                                         callback_data='yes'),
                                                    InlineKeyboardButton(text='Нет',
                                                                         callback_data='no')]])

kb_go_home = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='На главную',
                                                                         callback_data='go_home')]])

kb_reply_go_home = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='На главное меню')]],
                                       resize_keyboard=True,
                                       one_time_keyboard=True,
                                       input_field_placeholder='Выберите пункт...')
