from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.for_questions import get_yes_no_kb
from keyboards.for_service_single import service_kb
from keyboards.simple_row import make_row_keyboard

router = Router()

# Эти значения далее будут подставляться в итоговый текст, отсюда
# такая на первый взгляд странная форма прилагательных
regions = ["Чуй", "Ош", "Джалал-Абад", "Иссык-Куль", "Нарын", "Талас", "Баткен"]
cities = ["Бишкек", "Ош", "Джалал-Абад", "Каракол", "Талас", "Баткен", "Нарын"]
districts = ["Ленинский", "Центральный", "Джал", "Асанбай", "Орто-Сай", "Свердловский"]


class Register(StatesGroup):
    choosing_region = State()
    choosing_town = State()
    choosing_district = State()


@router.message(Command("registration"))
async def cmd_register(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите регион:", reply_markup=make_row_keyboard(regions)
    )
    # Устанавливаем пользователю состояние "выбирает region"
    await state.set_state(Register.choosing_region)


# Этап выбора city #


@router.message(Register.choosing_region, F.text.in_(regions))
async def region_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_region=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите город:",
        reply_markup=make_row_keyboard(cities),
    )
    await state.set_state(Register.choosing_town)


@router.message(Register.choosing_region)
async def region_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого региона.\n\n"
        "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(regions),
    )


# Этап выбора размера порции и отображение сводной информации #


@router.message(Register.choosing_town, F.text.in_(cities))
async def town_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_town=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали город {message.text.lower()} {user_data['chosen_town']}.\n"
        f"теперь выберите ваш район",
        reply_markup=make_row_keyboard(districts),
    )
    await state.set_state(Register.choosing_district)


@router.message(Register.choosing_town)
async def town_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого размера порции.\n\n"
        "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=make_row_keyboard(cities),
    )


@router.message(Register.choosing_district, F.text.in_(districts))
async def district_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_district=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали регион {user_data['chosen_region']}.\nВы выбрали город  {user_data['chosen_town']}.\nВы выбрали район {user_data['chosen_district']}.\n"
        f"теперь вы можете получить помощь по вашему району",
        # reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(
        text=f"Желаете ли вы продолжить и получить помощь по вашему району?",
        reply_markup=get_yes_no_kb(),
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()


@router.message(Text(text="да", ignore_case=True))
async def answer_yes(message: Message):
    await message.answer("Давайте начнем!", reply_markup=service_kb())


@router.message(Text(text="нет", ignore_case=True))
async def answer_no(message: Message):
    await message.answer("Жаль...", reply_markup=ReplyKeyboardRemove())


@router.message(Register.choosing_district)
async def district_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого района.\n\n"
        "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=make_row_keyboard(districts),
    )
