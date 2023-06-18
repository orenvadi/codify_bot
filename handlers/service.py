import random

from aiogram import F, Router
from aiogram.filters import Command, text
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.for_questions import get_yes_no_kb
from keyboards.for_service_single import service_kb
from keyboards.simple_row import make_row_keyboard

from .prompts import kindergarden_json, school_json, university_json

router = Router()

study_state = ["kindergarden", "school", "university"]
question_type = ["admission", "complaint", "reference"]


class Servicing(StatesGroup):
    choosing_study_state = State()
    choosing_question_type = State()


@router.message(Command("service"))
async def cmd_service(message: Message, state: FSMContext):
    await message.answer(
        text="выберите тип учреждения которое вам интересно",
        reply_markup=make_row_keyboard(study_state),
    )

    await state.set_state(Servicing.choosing_study_state)


@router.message(Servicing.choosing_study_state, F.text.in_(study_state))
async def study_state_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_study_state=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, тип обращения:",
        reply_markup=make_row_keyboard(question_type),
    )
    await state.set_state(Servicing.choosing_question_type)


@router.message(Servicing.choosing_study_state)
async def study_state_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого учебного заведения.\n\n"
        "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(study_state),
    )


@router.message(Servicing.choosing_question_type, F.text.in_(question_type))
async def study_state_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_question_type=message.text.lower())

    user_data = await state.get_data()

    glob_user_choses = set(
        [user_data["chosen_question_type"], user_data["chosen_study_state"]]
    )

    await message.answer(
        text="Спасибо. Теперь, вы получите помощь по данному вопросу",
        reply_markup=ReplyKeyboardRemove,
    )
    match user_data["chosen_study_state"]:
        case "kindergarden":
            ln = len(kindergarden_json["content"])
            l = random.randint(0, ln)
            txt = (
                kindergarden_json["content"][l]["prompt"]
                + "\n"
                + kindergarden_json["content"][l]["response"]
            )
        case "school":
            ln = len(school_json["content"])
            l = random.randint(0, ln)
            txt = (
                school_json["content"][l]["prompt"]
                + "\n"
                + school_json["content"][l]["response"]
            )
        case "university":
            ln = len(university_json["content"])
            l = random.randint(0, ln)
            txt = (
                university_json["content"][l]["prompt"]
                + "\n"
                + university_json["content"][l]["response"]
            )
        case _:
            txt = ""

    await message.answer(
        text=txt,
    )

    await state.clear()


@router.message(Servicing.choosing_study_state)
async def study_state_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого вида обращения.\n\n"
        "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(study_state),
    )
