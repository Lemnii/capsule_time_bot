import telebot
from telebot import types
from database import save_letter
from export_to_excel import export_letters_to_excel 

API_TOKEN = '7378588994:AAE_3YSAF5xxNGNqehL-W__fiLxJAajLK1o'  

bot = telebot.TeleBot(API_TOKEN)

user_data = {}  # Хранение временной информации о пользователе 

@bot.message_handler(commands=['start']) 
def send_start(message): 
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True) 
    start_button = types.KeyboardButton("Начать") 
    keyboard.add(start_button) 
    bot.send_message(message.chat.id, "Добро пожаловать! Нажмите 'Начать'", reply_markup=keyboard) 

@bot.message_handler(func=lambda message: message.text == "Начать") 
def ask_for_letter(message): 
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True) 
    letter_button = types.KeyboardButton("Написать письмо в капсулу времени") 
    keyboard.add(letter_button) 
    bot.send_message(message.chat.id, "Нажмите 'Написать письмо в капсулу времени'", reply_markup=keyboard) 

@bot.message_handler(func=lambda message: message.text == "Написать письмо в капсулу времени") 
def ask_name(message): 
    msg = bot.send_message(message.chat.id, "Введите ваши ФИО:") 
    bot.register_next_step_handler(msg, process_name_step) 

def process_name_step(message): 
    user_data['name'] = message.text 
    user_data['is_saved'] = False  # Устанавливаем значение по умолчанию для is_saved 
    msg = bot.send_message(message.chat.id, "Теперь напишите ваше письмо в будущее:") 
    bot.register_next_step_handler(msg, process_letter_step) 

def process_letter_step(message): 
    user_data['letter'] = message.text 
    name = user_data['name'] 
    letter = user_data['letter'] 

    # Создаем клавиатуру с кнопками
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True) 
    save_button = types.KeyboardButton("Сохранить") 
    cancel_button = types.KeyboardButton("Отмена") 
    keyboard.add(save_button, cancel_button) 


    formatted_message = (
        "Ваши данные:\nФИО: {name}\nПисьмо: {letter}\nВыберите действие:"
    ).format(name=name, letter=letter)

    bot.send_message(message.chat.id, formatted_message, reply_markup=keyboard, parse_mode="Markdown")

    # Регистрация обработчиков для кнопок
    bot.register_next_step_handler(message, lambda m: handle_user_action(m))

def handle_user_action(message):
    if message.text == "Сохранить":
        save_letter_handler(message)
    elif message.text == "Отмена":
        cancel_handler(message)

def save_letter_handler(message): 
    name = user_data['name']
    letter = user_data['letter']

    if user_data['is_saved']: 
        bot.send_message(message.chat.id, "Ваше письмо уже сохранено.") 
        ask_for_letter(message)
    else: 
        save_letter(name, letter)
        user_data['is_saved'] = True  # Устанавливаем флаг в True 
        bot.send_message(message.chat.id, "Спасибо! Ваша капсула сохранена!")
        ask_for_letter(message)

def cancel_handler(message): 
    if not user_data['is_saved']: 
        bot.send_message(message.chat.id, "Операция отменена.")
        ask_for_letter(message)  # Предлагаем начать заново
    else:
        bot.send_message(message.chat.id, "Ваше письмо уже сохранено. Хотите написать новое письмо?")
        ask_for_letter(message)  # Предлагаем начать заново

@bot.message_handler(commands=['export']) 
def export_data(message): 
    export_letters_to_excel() 
    bot.send_message(message.chat.id, "Данные успешно экспортированы в Excel!") 

bot.polling()