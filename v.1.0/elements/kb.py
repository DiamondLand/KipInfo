from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

priemka = "О приёмной комиссии"
supply_info = "Документы для подачи, сроки и этапы"
paid_info = "Стоимость обучения для договоров"
score_info = "Информация о среднем балле"
budget_info = "Количество мест"

# --- Главное меню --- #
def main_menu_kb() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text=priemka)], 
        [KeyboardButton(text=supply_info)],
        [KeyboardButton(text=paid_info)],
        [KeyboardButton(text=score_info)],
        [KeyboardButton(text=budget_info)]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
