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

    await message.answer(
        text=f"<b>СПРАВКА {hlink('KipHelper', 'https://t.me/ItcProjects')} v{message.bot.config['SETTINGS']['version']} — @ivan_abutkov:</b>\
            \n\n1. Данный бот использует расписание, составленное и отправленное учебной частью.\
            \n\n2. Чтобы посмотреть аудитории, выберите курс и группу. Будет показано актуальное расписание, составленное учебной частью.\
            \n\n3. Чтобы посмотреть расписание преподавателей, выберите ФИО преподавателя на кнопке. Страница включает в себя до 7 таких кнопок. Чтобы перейти на предыдущую или следующую страницу, используйте <b>'назад'</b> и <b>'вперёд'</b>, расположенные внизу панели.\
            \n\n4. Чтобы связаться с поддержкой бота, присоединитесь к <b>{hlink('каналу', 'https://t.me/ItcProjects')}</b> и задайте вопрос в нужном топике.\
            \n\n* <i>Бот является вспомогательным помощником для просмотра расписания, актуальное расписание и <b>все</b> актуальные изменения в расписании смотрите на официальных ресурсах колледжа.</i>\
            \n\n* <i>Также рекомендуем заглянуть в {hlink('KИПФИН | Общение', 'https://t.me/KipFinchikBot')}. Новые знакомства и приятное общение c аббитуриентами, выпускниками и студентами <u>КИПФИН</u>, <u>МФК</u>, <u>лицеем</u> ждут вас 💪💖!</i>"
    )
