import json

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums.chat_type import ChatType
from aiogram.utils.markdown import hlink

from functions.greeting import send_greeting

router = Router()


# --- Основная панель --- #
@router.message(Command("start", "schedule"))
async def start_cmd(message: Message):
    # Запрещаем доступ к команде если это группы
    if message.chat.type == ChatType.GROUP or message.chat.type == ChatType.SUPERGROUP:
        return

    await message.answer(text=f"{send_greeting(username=message.from_user.username)}\nЧётко сформулируйте ваш вопрос и напишите его в чат:")


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
        await message.answer(text=faq_text)

    except Exception as e:
        print(e)
        await message.answer(text="Произошла ошибка при генерации ЧаВо 🥺.")
