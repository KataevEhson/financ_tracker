from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from dotenv import load_dotenv 
from service import *
from conection import *
import asyncio
import os

load_dotenv()

token = os.getenv("BOT_TOKEN")

bot = Bot(token=token)
dp = Dispatcher()


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏁 старт")],
        [KeyboardButton(text="🆘 Помощь")],
    ],
    resize_keyboard=True,
)






@dp.message(F.text == "🏁 старт")
@dp.message(CommandStart())
async def start_bot(message: Message):
    if await  get_user_by_id(message.from_user.id):
        await message.answer(f"Асяляму алейкум @{message.from_user.username}  что привело тебя ко мне")
    else:
        user = message.from_user
        await create_user(user.username,  user.id)
        await message.answer(f"Асяляму алейкум  @{message.from_user.username}что привело тебя ко мне")



@dp.message(F.text == "🆘 Помощь")
@dp.message(Command("help"))
async def help_user(message : Message):
    await message.answer("""
======== У моего бота ест токие ващи ========
/start просто стартует
/help Помощ
/profile показывает твой профилъ
/withdraw пополнение поланса
/deposit снятие денег с баланса
/history показывает историю покупок
======== Вот и все болше ниче тут нету 😊 ========
""")






@dp.message(Command("profile"))
async def show_profile(message: Message):
    data = await profile(message.from_user.id)

    your_profile = (f"""
======== Ваш профилъ ========

        name: {data['username']}
        user_id: {data['telegram_id']}
        balance: {data['balance']}
    """)

    await message.answer(your_profile)


@dp.message(Command("withdraw"))
async def withdraw_money(message: Message, command: CommandObject):
    example = command.args.split("/")
    await withdraw(int(example[0]), message.from_user.id, example[1])
    await message.answer("Money taked successful")
   



@dp.message(Command("deposit"))
async def deposit_money(message: Message, command: CommandObject):
    example = command.args.split("/")
    await deposit(int(example[0]), message.from_user.id, example[1])
    await message.answer("Money given successful")    






@dp.message(Command("history"))
async def print_history(message : Message):
    data = await history()
    for i in data:
        yout_history = (f"""
======== Ваша история ========
        title: {i['title']}
        type: {i['type']}
        sum: {i['sum']}
    
""")
        await message.answer(yout_history)

async def main():
    await create_table()
    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())





