from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def service_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="/service")
    kb.adjust(1)
    return kb.as_markup(
        resize_keyboard=True, input_field_placeholder="Нажмите на кнопку"
    )
