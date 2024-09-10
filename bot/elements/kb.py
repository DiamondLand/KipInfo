from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

dod_info = "День открытых дверей (ДОД)"
general_info = "Общая информация"
communities_info = "Сообщества"
specialties_info = "Специальности"

# --- Главное меню --- #
def main_menu_kb() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text=dod_info)], 
        [KeyboardButton(text=communities_info)],
        [KeyboardButton(text=general_info)],
        [KeyboardButton(text=specialties_info)],
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
