import random
import string
import asyncio
from config import DB_PORT,DB_HOST,DB_NAME,DB_PASS,DB_USER, API_TOKEN
import psycopg2
from aiogram import Bot, Dispatcher, types



try:
    # connect to exist database
    connection = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        port=DB_PORT
    )
    connection.autocommit = True

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
# finally:
#     if connection:
#         # cursor.close()
#         connection.close()
#         print("[INFO] PostgreSQL connection closed")

def generate_random_string(length=6):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

async def start_command(message: types.Message):
    await message.answer("Hello! I'm a bot. Send me any message and I will reply with a random string.")

async def handle_message(message: types.Message):
    tg_id = message.from_user.id
    username = message.from_user.username
    print(username, tg_id)
    random_string = generate_random_string(6)
    with connection.cursor() as cursor:
        code = generate_random_string()
        cursor.execute(
            f"""INSERT INTO users (username, tg_id, code) VALUES
             ('{username}', '{tg_id}', '{code}');"""
         )
    await message.answer(random_string)

async def main() -> None:
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)

    dp.register_message_handler(start_command, commands='start')
    dp.register_message_handler(handle_message)

    await dp.start_polling()

asyncio.run(main())