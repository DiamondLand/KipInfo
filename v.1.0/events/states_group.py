from aiogram import Router
from aiogram.fsm.state import StatesGroup, State

router = Router()

# --- Админский StatesGroup для отправки рассылки --- #
class InsertMailingText(StatesGroup):
    text = State()
