import logging

from aiogram import Router
from aiogram.types import ErrorEvent
from aiogram.exceptions import (AiogramError, TelegramAPIError, CallbackAnswerException, SceneException, UnsupportedKeywordArgument,
                                TelegramNetworkError, TelegramRetryAfter, TelegramMigrateToChat, TelegramBadRequest, TelegramNotFound, TelegramConflictError,
                                TelegramUnauthorizedError, TelegramForbiddenError, TelegramServerError, RestartingTelegram, TelegramEntityTooLarge, ClientDecodeError)

router = Router()


# --- Обработчик ошибок --- #
@router.error()
async def errors_handler(event: ErrorEvent):
    # Предупреждения
    if isinstance(event.exception, UnsupportedKeywordArgument):
       logging.warning(f"UnsupportedKeywordArgument: {event.exception}")

    elif isinstance(event.exception, TelegramNetworkError):
       logging.warning("NetworkError")

    elif isinstance(event.exception, TelegramBadRequest):
        logging.warning(f"TelegramBadRequest: {event.exception}")

    elif isinstance(event.exception, TelegramNotFound):
        logging.warning(f"TelegramNotFound: {event.exception}")

    elif isinstance(event.exception, TelegramConflictError):
        logging.warning(f"TelegramConflictError: {event.exception}")

    elif isinstance(event.exception, TelegramServerError):
        logging.warning(f"TelegramServerError: {event.exception}")
        
    elif isinstance(event.exception, CallbackAnswerException):
        logging.warning(f"CallbackException: {event.exception}")

    elif isinstance(event.exception, SceneException):
        logging.warning(f"SceneException: {event.exception}")

    elif isinstance(event.exception, TelegramRetryAfter):
        logging.warning(f"TelegramRetryAfter: {event.exception}")

    elif isinstance(event.exception, TelegramMigrateToChat):
        logging.warning(f"TelegramMigrateToChat: {event.exception}")

    elif isinstance(event.exception, TelegramForbiddenError):
        logging.warning(f"TelegramForbiddenError: {event.exception}")

    elif isinstance(event.exception, TelegramEntityTooLarge):
        logging.warning(f"TelegramEntityTooLarge: {event.exception}")

    elif isinstance(event.exception, ClientDecodeError):
        logging.warning(f"ClientDecodeError: {event.exception}")

    # Ошибки
    elif isinstance(event.exception, AiogramError):
        logging.error(f"AiogramError: {event.exception}")

    elif isinstance(event.exception, TelegramAPIError):
        logging.error(f"TelegramAPIError: {event.exception}")
    
    elif isinstance(event.exception, TelegramUnauthorizedError):
        logging.error(f"TelegramUnauthorizedError: {event.exception}")
    
    elif isinstance(event.exception, RestartingTelegram):
        logging.error(f"RestartingTelegram: {event.exception}")
