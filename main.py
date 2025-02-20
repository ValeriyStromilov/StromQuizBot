import asyncio
import aiosqlite
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)

load_dotenv('key.env')
API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(API_TOKEN)
dp = Dispatcher()

DB_NAME = 'quiz_bot.db'

import data_read
from data_read import quiz_data
import keyboard_optns
from keyboard_optns import generate_options_keyboard

data_read
keyboard_optns

@dp.callback_query(F.data.in_({"right_answer", "wrong_answer"}))
async def handle_answer(callback: types.CallbackQuery):
    user_answer = None
    for row in callback.message.reply_markup.inline_keyboard:
        for button in row:
            if button.callback_data == callback.data:
                user_answer = button.text
                break
        if user_answer:
            break

    #убираем кнопку после ответа
    await callback.bot.edit_message_reply_markup(
        chat_id = callback.from_user.id,
        message_id = callback.message.message_id,
        reply_markup = None
    )

    current_question_index = await get_quiz_index(callback.from_user.id)
    #current_score = await get_user_score(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']
    correct_answer = quiz_data[current_question_index]['options'][correct_option]

    #правильный или неправильный ответ
    if callback.data == "right_answer":
        await callback.message.answer("Верно!")
        #current_score += 1
        #await update_user_score(callback.from_user.id, current_score)
    else:
        await callback.message.answer(f"Неверно! Вот правильный ответ: {correct_answer}")
    
    #обновление индекса вопроса
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        #await callback.message.answer(f"Это был последний вопрос! Вы ответили правильно на {current_score} вопросов из 12. Квиз завершён, спасибо за участие!")
        await callback.message.answer(f"Это был последний вопрос! Квиз завершён, спасибо за участие!")
        username = callback.from_user.username or callback.from_user.first_name #имя юзера
        score = current_question_index
        await upd_highscore(callback.from_user.id, username, score)
        await show_highscore(callback.message) #вывод таблицы рекордов

#хэндлер на команду "start"
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    new_score = 0
    await update_quiz_index(user_id, current_question_index)
    await update_user_score(user_id, new_score)
    await get_question(message, user_id)

async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

#async def get_user_score(user_id):
    #async with aiosqlite.connect(DB_NAME) as db:
        #async with db.execute('SELECT score FROM users WHERE user_id = ?', (user_id,)) as cursor:
            #results = await cursor.fetchone()
            #if results is not None:
                #return results[0]
            #else:
                #return 0

async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        await db.commit()

async def update_user_score(user_id, new_score):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT INTO users (user_id, score) VALUES (?, ?) ON CONFLICT (user_id) DO UPDATE SET score = excluded.score', (user_id, new_score))
        await db.commit()

#хэндлер на команду "quiz"
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer(f"Начинаем квиз!")
    await new_quiz(message)

#хэндлер на команду highscore, выводит таблицу рекордов
@dp.message(Command("highscore"))
async def cmd_highscore(message: types.Message):
    await show_highscore(message)

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, score INTEGER)''')
        await db.commit()

#список набравших наибольшее кол-во очков
async def upd_highscore(user_id: int, username: str, score: int):
    async with aiosqlite.connect(DB_NAME) as db:
        #Создаём/обновляем запись в таблице
        await db.execute('''INSERT OR REPLACE INTO users (user_id, username, score)
                         VALUES (?, ?, ?)''', (user_id, username, score))
        await db.commit()

#список набравших наибольшее кол-во очков
async def show_highscore(message: types.Message):
    async with aiosqlite.connect(DB_NAME) as db:
        #Вывод таблицу рекордов (топ-10 набравших кол-во очков)
        async with db.execute('''SELECT username, score FROM users ORDER BY score DESC LIMIT 10''') as cursor:
            leaders = await cursor.fetchall()
    
    #сообщение с выводом рекордов
    highscore_message = "Таблица рекордов:\n"
    for i, (username, score) in enumerate(leaders, start=1):
        highscore_message += "f{i}. {username}: {score} очков\n"

    #отправка сообщения
    await message.answer(highscore_message)

#хендлер на команду "help"
@dp.message(Command("help"))     
async def cmd_start(message: types.Message):
    await message.answer("Команды бота:\n start — запуск бота\n quiz — начало квиза\n help — справка, список комманд бота\n highscore — показать таблцу рекордов")

async def main():
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())