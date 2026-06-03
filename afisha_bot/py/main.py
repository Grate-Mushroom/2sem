import asyncio
import logging
import os
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import BOT_TOKEN, CACHE
from logging_middleware import LoggingMiddleware
from cinema_parser import get_movies_list_megakino, get_movie_all
from collage import create_movies_collage
from vk_client import get_vk_events
from reminder import add_reminder_to_file, check_reminders_loop

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.update.middleware(LoggingMiddleware())

MOVIES_PER_PAGE = 6

# Экранирование спецсимволов Markdown
def escape_md(text: str) -> str:
    if not text:
        return ""
    special_chars = r'_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{c}' if c in special_chars else c for c in text)

class CinemaStates(StatesGroup):
    choosing_day = State()
    choosing_movie = State()
    reminder_name = State()
    reminder_time = State()

# Главное меню
def get_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Кино в Кемерово", callback_data="menu_cinema")
    builder.button(text="События и афиша", callback_data="menu_vk")
    builder.adjust(1)
    return builder.as_markup()

# Клавиатура выбора даты
def get_dates_keyboard():
    today = datetime.today()
    builder = InlineKeyboardBuilder()

    for i in range(7):
        current_date = today + timedelta(days=i)
        day_num = current_date.day
        month_num = current_date.month

        if i == 0:
            text = "Сегодня"
        elif i == 1:
            text = "Завтра"
        else:
            text = f"{day_num:02d}.{month_num:02d}"

        builder.button(text=text, callback_data=f"date_{i}")

    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="Назад в меню", callback_data="main_menu"))
    return builder.as_markup()

# Обработка /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        "Я бот «Досуг 42». Чем займемся сегодня?",
        reply_markup=get_main_menu_keyboard()
    )


# Переход к выбору кино
@dp.callback_query(F.data == "menu_cinema")
async def cmd_cinema_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(CinemaStates.choosing_day)
    await callback.message.answer(
        "На какой день ищем сеансы?",
        reply_markup=get_dates_keyboard()
    )

# Показ событий из VK
@dp.callback_query(F.data == "menu_vk")
async def cmd_vk_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    events = await get_vk_events()

    if not events:
        await callback.message.answer("Не удалось найти события. Попробуйте позже.")
        return

    response_text = "События и афиша Кемерово:\n\n"

    for i, event in enumerate(events[:10], 1):
        title = escape_md(event['title'])
        description = escape_md(event['description'][:100])
        url = event['url']

        response_text += f"{i}. [*{title}*]({url})\n"
        response_text += f"   {event['date']} \n"
        response_text += f"   [{description}...]\n\n"
        response_text += f"   [Открыть пост]({url})\n\n"

    response_text += "Что делаем дальше?"
    await state.update_data(vk_events=events)

    builder = InlineKeyboardBuilder()
    builder.button(text="Создать напоминание", callback_data="vk_remind")
    builder.button(text="Назад в меню", callback_data="main_menu")
    builder.adjust(1)

    await callback.message.answer(
        response_text,
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

# Обработка выбора даты
@dp.callback_query(F.data.startswith("date_"))
async def process_day_choice(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    day_index = int(callback.data.split("_")[1])

    target_date = datetime.today() + timedelta(days=day_index)
    date_str = target_date.strftime("%Y/%m/%d")

    await state.update_data(chosen_day_index=day_index, chosen_date_str=date_str)

    if day_index == 0:
        day_text = "Сегодня"
    elif day_index == 1:
        day_text = "Завтра"
    else:
        day_text = target_date.strftime("%d.%m")

    loading = await callback.message.answer(
        f"Ищем сеансы на: *{day_text}*...",
        parse_mode="Markdown"
    )

    movies = await get_movies_list_megakino()

    if not movies:
        await loading.delete()
        await callback.message.answer("Не удалось загрузить афишу.")
        await state.clear()
        return

    await state.update_data(all_movies=movies, current_page=0)
    await loading.delete()
    await show_movies_page(callback, state, 0)

# Отображение страницы с фильмами
async def show_movies_page(callback: CallbackQuery, state: FSMContext, page: int):
    data = await state.get_data()
    movies = data.get('all_movies', [])

    if not movies:
        await callback.message.answer("Фильмы не найдены.")
        return

    total_pages = (len(movies) + MOVIES_PER_PAGE - 1) // MOVIES_PER_PAGE
    start_idx = page * MOVIES_PER_PAGE
    end_idx = min(start_idx + MOVIES_PER_PAGE, len(movies))
    page_movies = movies[start_idx:end_idx]

    collage_path = CACHE['collages'].get(page)

    if not collage_path or not os.path.exists(collage_path):
        collage_path = await create_movies_collage(page_movies, f"temp_collage_p{page}.jpg")
        if collage_path:
            CACHE['collages'][page] = collage_path

    text = f"Страница {page + 1} из {total_pages}\n\nВыберите фильм:"

    builder = InlineKeyboardBuilder()

    for i, movie in enumerate(page_movies):
        global_index = start_idx + i
        builder.button(text=movie['name'], callback_data=f"movie_{global_index}")

    builder.adjust(1, 1, 1, 1, 1, 1)

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="◀️", callback_data=f"page_{page-1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="▶️", callback_data=f"page_{page+1}"))

    if nav_buttons:
        builder.row(*nav_buttons)

    builder.row(
        InlineKeyboardButton(text="К выбору даты", callback_data="back_to_dates"),
        InlineKeyboardButton(text="В главное меню", callback_data="main_menu")
    )

    try:
        await callback.message.delete()
    except:
        pass

    if collage_path and os.path.exists(collage_path):
        photo_file = FSInputFile(collage_path)
        await callback.message.answer_photo(
            photo=photo_file,
            caption=text,
            reply_markup=builder.as_markup(),
            parse_mode="Markdown"
        )
    else:
        await callback.message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")

# Переключение страницы фильмов
@dp.callback_query(F.data.startswith("page_"))
async def process_page_change(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.replace("page_", ""))
    await callback.message.delete()
    await state.update_data(current_page=page)
    await show_movies_page(callback, state, page)

# Обработка выбора фильма
@dp.callback_query(F.data.startswith("movie_"))
async def process_movie_choice(callback: CallbackQuery, state: FSMContext):
    index_str = callback.data.replace("movie_", "", 1)
    movie_index = int(index_str)
    await callback.message.delete()

    data = await state.get_data()
    all_movies = data.get('all_movies', [])

    if movie_index >= len(all_movies):
        await callback.message.answer("Фильм не найден.")
        return

    movie = all_movies[movie_index]
    movie_name = movie['name']
    date_str = data.get('chosen_date_str', datetime.today().strftime("%Y/%m/%d"))

    loading = await callback.message.answer(
        f"Ищем расписание для: *{movie_name}*...",
        parse_mode="Markdown"
    )

    times = await get_movie_all(movie_name, date_str)
    await loading.delete()

    if not times:
        await callback.message.answer(
            f"Сеансов для *{movie_name}* не найдено.",
            parse_mode="Markdown"
        )
        current_page = data.get('current_page', 0)
        await show_movies_page(callback, state, current_page)
        return

    movie_name_escaped = escape_md(movie_name)
    response_text = f"*{movie_name_escaped}*\n\n"

    for cinema, sessions in times.items():
        cinema_escaped = escape_md(cinema)
        response_text += f"*{cinema_escaped}*:\n"
        for session in sessions:
            response_text += f"  {escape_md(session)}\n"
        response_text += "\n"

    response_text += "Что делаем дальше?"

    builder = InlineKeyboardBuilder()
    builder.button(text="Поставить напоминание", callback_data=f"remind_{movie_index}")
    builder.button(text="К списку фильмов", callback_data="back_to_movies")
    builder.button(text="В главное меню", callback_data="main_menu")
    builder.adjust(1)

    await callback.message.answer(
        response_text,
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )
    await state.set_state(CinemaStates.choosing_movie)

# Возврат к списку фильмов
@dp.callback_query(F.data == "back_to_movies")
async def back_to_movies(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.delete()
    await show_movies_page(callback, state, data.get('current_page', 0))

# Возврат к выбору даты
@dp.callback_query(F.data == "back_to_dates")
async def back_to_dates(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(CinemaStates.choosing_day)
    await callback.message.answer(
        "На какой день ищем сеансы?",
        reply_markup=get_dates_keyboard()
    )

# Начало создания напоминания из VK
@dp.callback_query(F.data == "vk_remind")
async def process_vk_reminder_request(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Введите название для напоминания:")
    await state.set_state(CinemaStates.reminder_name)

# Начало создания напоминания из расписания кино
@dp.callback_query(F.data.startswith("remind_"))
async def process_movie_reminder_request(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    await callback.message.answer(
        "Напоминание для фильма\n"
        "Введите название для напоминания:",
    )
    await state.set_state(CinemaStates.reminder_name)

# Получение названия напоминания
@dp.message(CinemaStates.reminder_name)
async def process_reminder_name(message: Message, state: FSMContext):
    reminder_name = message.text.strip()
    await state.update_data(reminder_name=reminder_name)

    reminder_name_escaped = escape_md(reminder_name)
    await message.answer(
        f"Название: *{reminder_name_escaped}*\n\n"
        f"Когда напомнить?\n"
        f"Формат: 18:00 или 15.06.2026 19:00",
        parse_mode="Markdown"
    )

    await state.set_state(CinemaStates.reminder_time)

# Получение времени напоминания
@dp.message(CinemaStates.reminder_time)
async def process_reminder_time(message: Message, state: FSMContext):
    reminder_time_text = message.text.strip()
    data = await state.get_data()
    reminder_name = data.get('reminder_name', 'Напоминание')

    try:
        reminder_time = None

        if "." in reminder_time_text and ":" in reminder_time_text:
            parts = reminder_time_text.split()
            date_part = parts[0]
            time_part = parts[1] if len(parts) > 1 else "00:00"
            day, month, year = map(int, date_part.split("."))
            hour, minute = map(int, time_part.split(":"))
            reminder_time = datetime(year, month, day, hour, minute)

        elif ":" in reminder_time_text:
            hour, minute = map(int, reminder_time_text.split(":"))
            reminder_time = datetime.today().replace(hour=hour, minute=minute, second=0)
            if reminder_time <= datetime.now():
                reminder_time += timedelta(days=1)

        else:
            raise ValueError("Неверный формат")

        await add_reminder_to_file(
            user_id=message.from_user.id,
            name=reminder_name,
            reminder_time_iso=reminder_time.isoformat()
        )

        await state.clear()

        builder = InlineKeyboardBuilder()
        builder.button(text="В главное меню", callback_data="main_menu")

        reminder_name_escaped = escape_md(reminder_name)
        reminder_time_formatted = reminder_time.strftime("%d.%m.%Y в %H:%M")

        await message.answer(
            f"*Напоминание создано!*\n\n"
            f"Название: {reminder_name_escaped}\n"
            f"Время: {reminder_time_formatted}\n\n"
            f"Бот напишет вам в это время.",
            reply_markup=builder.as_markup(),
            parse_mode="Markdown"
        )

    except Exception as e:
        print(f"Ошибка парсинга времени: {e}")
        await message.answer(
            "Не удалось распознать время. Попробуйте ещё раз:\n"
            "Формат: 18:00 или 15.06.2026 19:00",
            parse_mode="Markdown"
        )

# Возврат в главное меню
@dp.callback_query(F.data == "main_menu")
async def cmd_main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer(
        "Вы вернулись в главное меню.",
        reply_markup=get_main_menu_keyboard()
    )

# Запуск бота
async def main():
    asyncio.create_task(check_reminders_loop(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())