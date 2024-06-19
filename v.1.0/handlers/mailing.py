import asyncio

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from events.states_group import InsertMailingText

from database.services import get_users_service

router = Router()


# --- Обработчик сообщения и рассылка всем пользователям --- #
@router.message(InsertMailingText.text)
async def mailing_send(message: Message, state: FSMContext):
    msg = await message.answer(text="<b>💥💥 Процесс отправки будет запущен через <i>10 секунд</i>.</b>\nВы можете <b>отменить</b> это действие, вернувшись в /start или /info!")
    await asyncio.sleep(10) # Глушим на 10 секунд перед началом рассылки

    # Если пользоветель отмменил, то останавливаем рассылку
    if await state.get_state() != InsertMailingText.text:
        return

    # Получаем список всех анкет
    all_profiles = await get_users_service()
    counter = 0

    await msg.delete()
    await message.answer(text=f"<b>💥💥💥 Рассылка запущена!</b>")

    for user_id in all_profiles:
        try: # Пытаемся отправить соообщение пользователю
            await message.bot.send_message(
                chat_id=int(user_id['user_id']), 
                text=f"Рассылка от @{message.from_user.username}:\n—\n{message.text}"
            )
            counter += 1
        except:
            pass

    await message.answer(
        text=f"<b>Рассылка закончена!</b>\
            \n\nОтправлено {counter}/{len(all_profiles)}."
    )
