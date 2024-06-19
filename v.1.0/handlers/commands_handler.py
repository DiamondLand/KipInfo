import json
import psutil
import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink

from elements.kb import main_menu_kb

from functions.utilities import split_text
from functions.greeting import send_greeting

from database.services import get_users_service, get_or_create_user_service

from events.states_group import InsertMailingText

router = Router()

MAX_MESSAGE_LENGTH = 4096


# --- Основная панель --- #
@router.message(Command("start"))
async def start_cmd(message: Message, state: FSMContext):
    # Если стадия существует, выходим из неё
    if await state.get_state() is not None:
        await state.clear()

    try:
        await get_or_create_user_service(user_id=message.from_user.id)
    except Exception as _ex:
        logging.warning(f"Не удалось проверить аккаунт! {_ex}")

    try:
        with open('assets/questions.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        questions_and_answers = data['questions_and_answers']

        await message.answer(text=f"{send_greeting(username=message.from_user.username)}\n<b>Вас приветствует бот приёмной комиссии КИПФИН!</b>\n\n{questions_and_answers[1]['answer']}")
    except Exception as _e:
        logging.error(_e)

    await message.answer(
        text=f"<i>* Рекомендуем заглянуть в {hlink('KИПФИН | Общение', 'https://t.me/KipFinchikBot')}. Новые знакомства и приятное общение c аббитуриентами, выпускниками и студентами <u>КИПФИН</u>, <u>МФК</u>, <u>лицеем</u> ждут вас 💪💖!"
    )
    await message.answer(
        text=f"Чётко сформулируйте ваш вопрос и напишите его в чат, либо же выберите по кнопкам ниже:",
        reply_markup=main_menu_kb()
    )


# --- Информационнная панель --- #
@router.message(Command("info"))
async def info_cmd(message: Message, state: FSMContext):
    # Если стадия существует, выходим из неё
    if await state.get_state() is not None:
        await state.clear()

    try:
        with open('assets/questions.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        questions_and_answers = data['questions_and_answers']

        faq_list = []
        for index, qa in enumerate(questions_and_answers, start=1):
            faq_list.append(
                f"<code>{index}. Вопрос:</code>\n<i>{qa['question']}</i>\n<code>Ответ на вопрос:</code>\n<i>{qa['answer']}</i>\n")

        faq_text = "\n\n".join(faq_list)

        text_chunks = split_text(faq_text, MAX_MESSAGE_LENGTH)
        for chunk in text_chunks:
            await message.answer(text=chunk)
    except Exception as _ex:
        logging.error(_ex)
        await message.answer(text="Произошла ошибка при генерации ЧаВо 🥺.")


# --- Статистика --- #
@router.message(Command("statistic", "bin"))
async def statistic_cmd(message: Message, state: FSMContext):
    if int(message.from_user.id) not in map(int, [767922691, 872278858]):
        return

    # Если стадия существует, выходим из неё
    if await state.get_state() is not None:
        await state.clear()

    users_count = f"<b>Пользователей:</b> <code>{len(await get_users_service())}</code>"
    await message.answer(text=f"<b>СТАТИСТИКА:</b>\
                            \n\n{users_count}\
                            \n\n<b>CPU:</b> <code>{psutil.cpu_percent(interval=1)}</code> | <b>RAM:</b> <code>{psutil.virtual_memory().percent}</code>%\
                            \n<b>Использовано дискового пространства:</b> <code>{psutil.disk_usage('/').percent}</code>%"
    )


# --- Перейти в рассылку -> Написать текст --- #
@router.message(Command("mailing", "bin2"))
async def mailing_cmd(message: Message, state: FSMContext):
    if int(message.from_user.id) not in map(int, [767922691, 872278858]):
        return

    # Если стадия существует, выходим из неё
    if await state.get_state() is not None:
        await state.clear()

    await message.answer(text="💥 Введите текст, который будет отправлен всем пользователям:")
    await state.set_state(InsertMailingText.text)
