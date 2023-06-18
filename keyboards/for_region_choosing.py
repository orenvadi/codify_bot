from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def region_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Чуй")
    kb.button(text="Ош")
    kb.button(text="Джалал-Абад")
    kb.button(text="Иссык-Куль")
    kb.button(text="Нарын")
    kb.button(text="Талас")
    kb.button(text="Баткен")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)
