from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Выберите, что хотите сделать: "
        "зарегистрироваться (/registration) или умереть (/die).",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command(commands=["die"]))
@router.message(Text(text="отмена", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено вы умерли", reply_markup=ReplyKeyboardRemove()
    )
