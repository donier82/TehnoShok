import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from config import token

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher()

start_buttons = [
    [KeyboardButton(text='О нас')],
    [KeyboardButton(text='Товары')],
    [KeyboardButton(text='Заказать')],
    [KeyboardButton(text='Контакты')],
]
start_keyboard = ReplyKeyboardMarkup(keyboard=start_buttons, resize_keyboard=True)

# Словарь для хранения временных данных о заказах
order_data = {}

# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(f"Здравствуйте, {message.from_user.full_name}!", reply_markup=start_keyboard)

@dp.message(F.text == 'О нас')
async def about_us(message: Message):
    await message.answer("Tehno-shop - Это магазин ТВ. Мы открылись недавно ")

# Кнопки меню товаров
product_buttons = [
    [KeyboardButton(text="Samsung")],
    [KeyboardButton(text="Xiaomi")],
    [KeyboardButton(text="Sumsung UHD")],
    [KeyboardButton(text="Sumsung ULTRA")],
    [KeyboardButton(text="Sumsung ANDROID")],
    [KeyboardButton(text="Назад")]
]
product_keyboard = ReplyKeyboardMarkup(keyboard=product_buttons, resize_keyboard=True)

# Обработчик кнопки "Товары"
@dp.message(F.text == 'Товары')
async def all_goods(message: Message):
    await message.answer("Вот наши товары", reply_markup=product_keyboard)

# Обработчики для каждого товара
@dp.message(F.text == 'Samsung')
async def samsung_info(message: Message):
    await message.answer_photo('https://leonardo.osnova.io/a85ff9ac-16eb-5e81-afcf-340ec6076cfc/-/preview/592x/-/format/webp')
    await message.answer("Samsung \nЦена - 24000\nАртикул - 1")

@dp.message(F.text == 'Xiaomi')
async def redmi_info(message: Message):
    await message.answer_photo('https://leonardo.osnova.io/a0606799-71a7-5d17-a375-e8e497579921/-/preview/1800x/')
    await message.answer("Xiaomi TV A Pro 55\nЦена - 19000\nАртикул - 2")

@dp.message(F.text == 'Sumsung UHD')
async def iphone_info(message: Message):
    await message.answer_photo('https://leonardo.osnova.io/b9e1870c-d1d3-5927-842b-0681eaa0637a/-/preview/1900x/')
    await message.answer("Sumsung UHD\nЦена - 33000\nАртикул - 3")

@dp.message(F.text == 'Sumsung ULTRA')
async def iphone_info(message: Message):
    await message.answer_photo('https://leonardo.osnova.io/1853baba-5635-504f-af6b-fddddc8aa2e5/-/preview/1800x/')
    await message.answer("Sumsung ULTRA\nЦена - 33000\nАртикул - 4")

@dp.message(F.text == 'Sumsung ANDROID')
async def iphone_info(message: Message):
    await message.answer_photo('https://leonardo.osnova.io/65fba61c-2cbc-5844-93e4-71fd2ca2e4f2/-/preview/592x/-/format/webp')
    await message.answer("Sumsung ANDROID\nЦена - 33999\nАртикул - 5")


@dp.message(F.text == 'Назад')
async def back_to_start(message: Message):
    await message.answer("Вы вернулись в главное меню", reply_markup=start_keyboard)

@dp.message(F.text == 'Заказать')
async def order(message: Message):
    user_id = message.from_user.id
    order_data[user_id] = {'step': 'waiting_for_articul'}
    await message.answer("ВВедите артикул телевизора:")

@dp.message(lambda message: message.from_user.id in order_data and order_data[message.from_user.id]['step'] == 'waiting_for_articul')
async def process_articul(message: Message):
    user_id = message.from_user.id
    order_data[user_id]['articul'] = message.text
    order_data[user_id]['step'] = 'waiting_for_contact'
    await message.answer("Пожалуйста, поделитесь вашим контактом", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Поделиться контактом", request_contact=True)]],
        resize_keyboard=True
    ))

@dp.message(F.contact)
async def get_contact(message: Message):
    user_id = message.from_user.id


    if user_id in order_data and order_data[user_id]['step'] == 'waiting_for_contact':
        contact_info = f"Имя: {message.contact.first_name}\nФамилия: {message.contact.last_name}\nТелефон: {message.contact.phone_number}"
        
        try:
            await bot.send_message(chat_id=-4255458461, text=contact_info)  
            await message.answer("Спасибо, что заказали наш товар!")
        except Exception as e:
            logging.error(f"Ошибка отправки сообщения: {e}")
            await message.answer("Произошла ошибка при обработке вашего заказа.")
        
        await message.answer("Вы вернулись на главное меню", reply_markup=start_keyboard)
        del order_data[user_id]
    else:
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте снова.")

@dp.message(F.text == 'Контакты')
async def contacts(message: Message):
    await message.answer("Контакты Tehno-shop:\nТелефон: +996 552230335\nEmail: tehno-shop@.kg")

# Запуск бота
async def main():
    await bot.delete_webhook() 
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
