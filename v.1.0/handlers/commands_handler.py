import json
import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums.chat_type import ChatType

from elements.kb import main_menu_kb
from functions.greeting import send_greeting

router = Router()

MAX_MESSAGE_LENGTH = 4096


def split_text(text, max_length):
    chunks = []
    while len(text) > max_length:
        split_index = text.rfind('\n\n', 0, max_length)
        if split_index == -1:
            split_index = max_length
        chunks.append(text[:split_index])
        text = text[split_index:]
    chunks.append(text)
    return chunks


# --- Основная панель --- #
@router.message(Command("start", "schedule"))
async def start_cmd(message: Message):
    # Запрещаем доступ к команде если это группы
    if message.chat.type == ChatType.GROUP or message.chat.type == ChatType.SUPERGROUP:
        return

    await message.answer(
        text=f"{send_greeting(username=message.from_user.username)}\nВас приветствует бот приёмной комиссии КИПФИН!\n\nЧётко сформулируйте ваш вопрос и напишите его в чат или же выберите по кнопкам ниже:",
        reply_markup=main_menu_kb()
    )


# --- Информационнная панель --- #
@router.message(Command("info"))
async def info_cmd(message: Message):
    # Запрещаем доступ к команде если это группы
    if message.chat.type == ChatType.GROUP or message.chat.type == ChatType.SUPERGROUP:
        return

    try:
        with open('assets/questions.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        questions_and_answers = data["questions_and_answers"]
        
        faq_list = []
        for index, qa in enumerate(questions_and_answers, start=1):
            question = qa["question"]
            answer = qa["answer"]
            faq_list.append(f"<code>{index}. Вопрос:</code>\n<i>{question}</i>\n<code>Ответ на вопрос:</code>\n<i>{answer}</i>\n")
        
        faq_text = "\n\n".join(faq_list)

        text_chunks = split_text(faq_text, MAX_MESSAGE_LENGTH)
        for chunk in text_chunks:
            await message.answer(text=chunk)

    except Exception as _ex:
        logging.error(_ex)
        await message.answer(text="Произошла ошибка при генерации ЧаВо 🥺.")
